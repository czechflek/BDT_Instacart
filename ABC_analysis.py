import commands

def executeQuery(query, outputFormat):
    result_string = 'beeline -u "jdbc:hive2://hador-c1.ics.muni.cz:10000/instacart;principal=hive/hador-c1.ics.muni.cz@ICS.MUNI.CZ" ' \
        '--fastConnect=true --showHeader=false --verbose=false --showWarnings=false --silent=true --outputformat=' + outputFormat + ' ' \
        ' -e "' + query + ';"'

    status, output = commands.getstatusoutput(result_string)

    if status == 0:
        return output
    else:
        error = "Error encountered while executing query: " + query
        print error


def getTotalOrders():
    query = 'select count(*) from order_products'
    totalStr = executeQuery(query, "csv")

    return int(totalStr[1:len(totalStr)-1])


def getClass(fromPercent, toPercent, total):
    fromId = int(total * fromPercent) + 1
    toId = int(total * toPercent) + 1

    query = """
        SELECT filtered.product_name, COUNT(filtered.product_name) AS Products_in_Class
        FROM (
            SELECT p.product_name, ps.Number_of_Orders
            FROM products_ordered_vw AS ps
            left join products as p
                on p.product_id == ps.product_id
            WHERE ps.rowid >= """ + str(fromId) + """ AND ps.rowid < """ + str(toId) + """
            ) AS filtered
        GROUP BY filtered.product_name
        ORDER BY Products_in_Class DESC
        LIMIT 5;
    """

    return executeQuery(query, "table")


total = getTotalOrders()

classA = getClass(0.8, 1.0, total)
classB = getClass(0.5, 0.8, total)
classC = getClass(0.0, 0.5, total)

print "Class A:"
print classA

print "Class B:"
print classB

print "Class C:"
print classC
