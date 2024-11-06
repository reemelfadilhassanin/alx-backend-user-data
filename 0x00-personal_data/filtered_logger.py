#!/usr/bin/env python3
import re

def filter_datum(fields, redaction, message, separator):
    """
    Function to obfuscate specific fields in a log message.
    
    Arguments:
    fields: List of strings representing field names to obfuscate
    redaction: The string to replace the fields with
    message: The log message string
    separator: The separator character used in the log message
    
    Returns:
    The obfuscated log message.
    """
    return re.sub(r'({}=[^{}]*{})'.format('|'.join(fields), separator, separator), 
                  lambda m: m.group(0).replace(m.group(1).split('=')[0] + '=', m.group(1).split('=')[0] + '=' + redaction), 
                  message)
