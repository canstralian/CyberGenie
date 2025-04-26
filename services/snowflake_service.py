import snowflake.connector
from flask import current_app

class SnowflakeService:
    def __init__(self):
        """
        Initializes the SnowflakeService. The class manages the connection 
        to the Snowflake database and provides methods for interacting with it.
        """
        self.conn = None

    def connect(self):
        """
        Establishes a connection to the Snowflake database using configuration 
        parameters stored in Flask's `current_app.config`. If a connection already 
        exists, it returns the existing connection; otherwise, it creates a new one.
        
        Returns:
            snowflake.connector.connection.SnowflakeConnection or None: 
            The Snowflake connection object or None if the connection failed.
        """
        if not self.conn:
            try:
                # Attempt to establish a connection
                self.conn = snowflake.connector.connect(
                    user=current_app.config['SNOWFLAKE_USER'],
                    password=current_app.config['SNOWFLAKE_PASSWORD'],
                    account=current_app.config['SNOWFLAKE_ACCOUNT'],
                    database=current_app.config['SNOWFLAKE_DATABASE'],
                    port=current_app.config['SNOWFLAKE_PORT']
                )
                current_app.logger.info("Successfully connected to Snowflake.")
            except Exception as e:
                # Log and return None in case of connection failure
                current_app.logger.error(f"Failed to connect to Snowflake: {str(e)}")
                self.conn = None
        return self.conn

    def close_connection(self):
        """
        Closes the Snowflake connection if it exists. This method should be called 
        when the connection is no longer needed to free up resources.
        """
        if self.conn:
            try:
                self.conn.close()
                current_app.logger.info("Snowflake connection closed successfully.")
            except Exception as e:
                current_app.logger.error(f"Failed to close Snowflake connection: {str(e)}")
            finally:
                self.conn = None

    def store_finding(self, finding):
        """
        Stores a vulnerability finding in the Snowflake database. This method 
        inserts data into the `findings` table, using parameterized queries 
        to avoid SQL injection risks.

        Args:
            finding (object): An object containing scan results and vulnerability details.

        Raises:
            Exception: In case of failure to store the finding in the database.
        """
        conn = self.connect()
        if conn is None:
            raise Exception("Database connection not established.")
        
        try:
            cursor = conn.cursor()
            sql = """
            INSERT INTO findings (scan_id, vulnerability_type, severity, description, proof_of_concept)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                finding.scan_id,
                finding.vulnerability_type,
                finding.severity,
                finding.description,
                finding.proof_of_concept
            ))
            conn.commit()
            current_app.logger.info(f"Successfully stored finding for scan ID {finding.scan_id}.")
        except Exception as e:
            current_app.logger.error(f"Failed to store finding for scan ID {finding.scan_id}: {str(e)}")
            raise  # Re-raise the exception after logging it
        finally:
            # Ensure cursor is closed
            cursor.close()

    def reconnect(self):
        """
        Attempts to re-establish the connection to Snowflake if the current 
        connection has failed or been closed.
        
        Returns:
            snowflake.connector.connection.SnowflakeConnection or None: 
            The new Snowflake connection object or None if the reconnection failed.
        """
        self.close_connection()
        return self.connect()

# This file is formatted using black
