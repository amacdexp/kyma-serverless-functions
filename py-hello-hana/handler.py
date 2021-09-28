import os
def main(event, context):
    return "Hello Hana User [" + os.environ['DB_USERNAME']  + "] it works"