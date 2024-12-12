import snowflake.connector
from flask import current_app

class SnowflakeService:
    def __init__(self):
        self.conn = None

    def connect(self):
        if not self.conn:
            try:
                self.conn = snowflake.connector.connect(
                    user=current_app.config['SNOWFLAKE_USER'],
                    password=current_app.config['SNOWFLAKE_PASSWORD'],
                    account=current_app.config['SNOWFLAKE_ACCOUNT'],
                    database=current_app.config['SNOWFLAKE_DATABASE'],
                    port=current_app.config['SNOWFLAKE_PORT']
                )
                return self.conn
            except Exception as e:
                current_app.logger.error(f"Failed to connect to Snowflake: {str(e)}")
                # Return None instead of failing to allow the app to start
                return None
        return self.conn

    def store_finding(self, finding):
        conn = self.connect()
        cursor = conn.cursor()
        
        sql = """
        INSERT INTO findings (scan_id, vulnerability_type, severity, description)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (
            finding.scan_id,
            finding.vulnerability_type,
            finding.severity,
            finding.description
        ))
        conn.commit()
