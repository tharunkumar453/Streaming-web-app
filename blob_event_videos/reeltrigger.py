# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(reeltrigger) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints
import logging
import azure.functions as func

reeltrigger = func.Blueprint()


@reeltrigger.event_grid_trigger(arg_name="azeventgrid")
def reeltrigger(azeventgrid: func.EventGridEvent):
    logging.info('Python EventGrid trigger processed an event')
