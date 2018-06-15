import db_connection

class TestingRepository:
    def set_amp_test_info(self, model, serial_number, notes):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO qcTestAmp (model, serialNumber, note, dateChecked)
                VALUES(%s, %s, %s, CURDATE())
                """
                cursor.execute(sql, (model, serial_number, notes))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def set_amp_voltage_measurement_10_percent(self, voltage, bias, plate, screen, filament, serial_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                UPDATE qcTestAmp
                SET
                    voltageAC10Percent = %s,
                    bias10Percent = %s,
                    tubePlate10Percent = %s,
                    tubeScreen10Percent = %s,
                    filament10Percent = %s
                WHERE serialNumber = %s
                """
                cursor.execute(sql, (voltage, bias, plate, screen, filament, serial_number))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def set_amp_voltage_measurement_30_percent(self, voltage, bias, plate, screen, filament, serial_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                UPDATE qcTestAmp
                SET
                    voltageAC30Percent = %s,
                    bias30Percent = %s,
                    tubePlate30Percent = %s,
                    tubeScreen30Percent = %s,
                    filament30Percent = %s
                WHERE serialNumber = %s
                """
                cursor.execute(sql, (voltage, bias, plate, screen, filament, serial_number))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def set_amp_voltage_measurement_87_percent(self, voltage, bias, plate, screen, filament, serial_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                UPDATE qcTestAmp
                SET
                    voltageAC87Percent = %s,
                    bias87Percent = %s,
                    tubePlate87Percent = %s,
                    tubeScreen87Percent = %s,
                    filament87Percent = %s
                WHERE serialNumber = %s
                """
                cursor.execute(sql, (voltage, bias, plate, screen, filament, serial_number))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def set_amp_voltage_measurement_100_percent(self, voltage, bias, plate, screen, filament, serial_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                UPDATE qcTestAmp
                SET
                    voltageAC100Percent = %s,
                    bias100Percent = %s,
                    tubePlate100Percent = %s,
                    tubeScreen100Percent = %s,
                    filament100Percent = %s
                WHERE serialNumber = %s
                """
                cursor.execute(sql, (voltage, bias, plate, screen, filament, serial_number))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def set_amp_power_handling(self, power30, power1k, power30k, serial_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                UPDATE qcTestAmp
                SET
                    power30Hz = %s,
                    power1kHz = %s,
                    power30kHz = %s
                WHERE serialNumber = %s
                """
                cursor.execute(sql, (power30, power1k, power30k, serial_number))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()