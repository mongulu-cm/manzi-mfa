from unittest.mock import patch
import os
import unittest
from unittest.mock import patch, MagicMock
from notifier.sms_notifier import connect_to_db, get_users_to_notify  # Replace 'notifier.sms_notifier' with the actual name of your script file

class TestDatabaseConnection(unittest.TestCase):
    @patch('notifier.sms_notifier.psycopg2.connect')
    def test_connect_to_db(self, mock_connect):
        # Test the database connection function
        connect_to_db()
        mock_connect.assert_called_once()

class TestGetUsersToNotify(unittest.TestCase):
    @patch('notifier.sms_notifier.psycopg2.connect')
    def test_get_users_to_notify(self, mock_connect):
            # Mock database connection
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            # Mock __enter__ and __exit__ for the cursor context manager
            mock_cursor.__enter__.return_value = mock_cursor
            mock_cursor.__exit__.return_value = None
            
            # Mock data to be returned by cursor.fetchall
            mock_cursor.fetchall.return_value = [
                (1, 'user1', '2023-11-05 10:00:00', 'event1'),
                (2, 'user2', '2023-11-05 11:00:00', 'event2'),
            ]

            # Get the mock connection
            connection = connect_to_db()

            # Call the function to test
            users = get_users_to_notify(connection)

            # Ensure the cursor was used to execute a query
            mock_cursor.execute.assert_called_once()

            # Check the returned value
            self.assertEqual(len(users), 2)  # replace 2 with the expected number of users to be notified based on your mock data

            # Ensure the connection cursor is closed
            mock_conn.close.assert_called_once()
