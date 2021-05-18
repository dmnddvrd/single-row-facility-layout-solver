import pysftp

class SftpStorage(object):

    def __init__(self, host, username):
        # Define the remote path where the file will be uploaded
        self.cnopts = pysftp.CnOpts()
        # This is set to none for easier usage, with a live server we would need to enable handshake
        self.cnopts.hostkeys, self.host, self.username, self.private_key = None, host, username, private_key



    def upload_file(self, local_file, destionation_path: str):
        with pysftp.Connection(
                host=self.host,
                username=self.username,
                private_key=self.private_key,
                cnopts=self.cnopts
        ) as sftp:
            local_file_path = local_file
            print(f'Uploading output file: {local_file_path} to remote location: {destionation_path}')
            sftp.put(
                localpath=local_file_path,
                remotepath=destionation_path,
                confirm=False
            )
