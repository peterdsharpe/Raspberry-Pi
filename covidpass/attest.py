from covidpass import *

if __name__ == '__main__':
    with Session(read_credentials()) as session:
        submit_attestation(session)
