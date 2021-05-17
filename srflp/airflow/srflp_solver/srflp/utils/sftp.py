import pysftp
import os


class SftpStorage(object):
    
    def upload_file(self, file_name: str):
        # Define the remote path where the file will be uploaded
        remote_file_path = f"{os.environ.get('SFTP_UPLOAD_PATH')}{file_name}"
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        with pysftp.Connection(
                host=os.environ.get('SFTP_HOSTNAME'),
                username=os.environ.get('SFTP_USERNAME'),
                private_key='id_rsa',
                cnopts=cnopts
        ) as sftp:
            local_file_path = f"{os.environ.get('TMP_PATH')}{file_name}"
            self._logging.log(f'Uploading output file: {local_file_path} to remote location: {remote_file_path}')

            sftp.put(
                localpath=local_file_path,
                remotepath=remote_file_path,
                confirm=False
            )
