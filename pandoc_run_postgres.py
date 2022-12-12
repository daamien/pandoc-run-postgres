#!/usr/bin/env python3

"""
Execute SQL queries inside a Markdown document
"""

import psycopg
import sqlparse
import panflute as pf

##
## Constants
##
FILTER_NAME='pandoc-psql'


# We don't open the global connection right away
# Instead we wait until we find a least one `run-postgres`
# code blocks in the doc
GLOBAL_CONN = None

def get_str_option(element, doc, tag, default):
    """
    Parse a string option
    """
    options=element.attributes if element else None
    return pf.get_option(  options=options,
                        local_tag=tag,
                        doc=doc,
                        doc_tag=f"{FILTER_NAME}.{tag}",
                        default=default,
                        error_on_none=False)

def get_bool_option(element, doc, tag, default):
    """
    Parse a boolean option
    """
    return get_str_option(  element,
                            doc,
                            tag,
                            default
           ).lower() in ("yes", "true", "t", "1")

def get_list_option(element, doc, tag, default, separator=','):
    """
    Parse a list option
    """
    return get_str_option(element,doc,tag,default).split(separator)

def panflute_row_factory(cursor):
    """
    Psycopg Row Factory
    """
    return get_panflute_row

def get_panflute_cell(value):
    """
    Each value of the SQL row becomes a Markdown table cell
    """
    return pf.TableCell(pf.Plain(pf.Str(str(value))))

def get_panflute_row(values):
    """
    Transform a SQL table tuple into a Markdown table row
    """
    return pf.TableRow(*[get_panflute_cell(v) for v in values])

def get_panflute_table(conn, query, show_result):
    """
    Run a query and tranform the result into a Markdown table
    """
    with conn.cursor(row_factory=panflute_row_factory) as cur:
        cur.execute(query)
        # if the query returns nothing, then cur.description is None
        if (show_result and cur.description):
            column_names = pf.TableRow(*[get_panflute_cell(i[0]) for i in cur.description])
            cells = cur.fetchall()
            return pf.Table(   pf.TableBody(*cells),
                            head=pf.TableHead(column_names),
                            caption=pf.Caption())
    return None


def action(options, data, element, doc):
    """
    For each `run-postgres` code block:
        * run the query
        * output the query as an SQL code block
        * output the result as a table
    """

    output = []

    ##
    ## Code Block parameters
    ## /!\ do not confuse with `options`
    ##
    params={}
    params['classes']=get_list_option(element, doc,"class", 'sql',' ')
    params['parse_query']=get_bool_option(element, doc,"parse_query", 'True')
    params['show_query']=get_bool_option(element, doc,"show_query", 'True')
    params['show_result']=get_bool_option(element, doc,"show_result", 'True')

    ##
    ## Connection info
    ##
    ## This is used when user wants to overide the global connection
    ## and open a separate ("local") connection for each codeblock
    ##
    local={}
    local['dbname']=get_str_option(element, doc,"dbname", None)
    local['user']=get_str_option(element, doc,"user", None)
    local['password']=get_str_option(element, doc,"password", None)
    local['host']=get_str_option(element, doc,"host", None)
    local['port']=get_str_option(element, doc,"port", None)

    # In this case, `options` is not a dict, it's the actual SQL query
    query = str(options)

    ##
    ## Step 1 : Write the Query
    ##
    if params['show_query']:
        if params['parse_query']:
            query = sqlparse.format(query, reindent=True, keyword_case="upper")
        output.append(pf.CodeBlock(query,classes=params['classes']))

    ##
    ## Step 2 : Execute the Query and display the result
    ##
    global GLOBAL_CONN
    local_conn=None
    try:
        ## if at least one local param is provided
        ## then open a one-shot connection
        conninfo=psycopg.conninfo.make_conninfo('',**local)
        if conninfo:
            local_conn = psycopg.connect(conninfo,autocommit=True)
            conn = local_conn

        ## else use the global connection
        else:
            if not GLOBAL_CONN:
                ## The global connection is not initialized,
                ## read the PG ENV variables and open it
                GLOBAL_CONN = psycopg.connect(autocommit=True)
            conn = GLOBAL_CONN

        result=get_panflute_table(conn, query, params['show_result'])
        if result:
            output.append(result)

    except Exception as err:
        div=pf.Div(attributes={'class': 'warning'})
        div.content=pf.convert_text(f"pandoc-run-postgres: {err}")
        output.append(div)

    finally:
        if local_conn:
            local_conn.close()

    return output



if __name__ == "__main__":
    # We don't open the global connection right away
    # Instead we wait until we find a least one `run-postgres`
    # code blocks in the doc
    pf.run_filter(pf.yaml_filter, tag='run-postgres', function=action)
    if GLOBAL_CONN:
        GLOBAL_CONN.close()
