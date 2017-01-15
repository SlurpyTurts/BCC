from bcc.dataaccess import db_connection


def test_can_run_select_query():
    connection = db_connection.get_connection()

    try:

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * from bcc.inventory limit %s"
            cursor.execute(sql, 10)
            result = cursor.fetchmany()
            for record in result:
                print record

            assert result
    finally:
        connection.close()
