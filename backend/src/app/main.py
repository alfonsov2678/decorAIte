from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    # GET A REQUEST, YOU HAVE THE FOLLOWING INPUTS
    # SOURCE IMAGE: SOURCE IMAGE
    # BOUNDING BOX: ON SOURCE IMAGE
    # QUERY
    
    # STEP ONE: RETRIEVE ALL RELEVANT ITEMS FROM THE QUERY
    
    
    # STEP TWO: CALL CONTROLNET API MULTIPLE TIMES TO CREATE MULTIPLE RENDERS AND RETURN 
    
    
    
    return {"message": "Hello World"}