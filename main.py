import asyncio
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from database import connect_db, close_db, connect_ai_db, close_ai_db
from routers import auth, caregiver, elder, service_provider, disease_information, drug_information, food_information, herb_information, drug_foodherb_interaction, medical_document, service, medicine, daily_medicine, notification, user
from dependencies import get_current_user
from utils.firebase import init_firebase
from utils.notification_cron import notification_cron_job
import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    await connect_ai_db()
    init_firebase()
    cron_task = asyncio.create_task(notification_cron_job())
    yield
    cron_task.cancel()
    await close_db()
    await close_ai_db()

from utils.rate_limiter import rate_limit_dependency

app = FastAPI(lifespan=lifespan, title="SenioCare API", dependencies=[Depends(rate_limit_dependency)])

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Protected Routes
app.include_router(
    caregiver.router, 
    prefix="/caregivers", 
    tags=["Caregivers"], 
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    elder.router, 
    prefix="/elders", 
    tags=["Elders"], 
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    service_provider.router, 
    prefix="/service-providers", 
    tags=["Service Providers"], 
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    medical_document.router,
    prefix="/medical-documents",
    tags=["Medical Documents"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    service.router,
    prefix="/services",
    tags=["Services"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    medicine.router,
    prefix="/medicines",
    tags=["Medicines"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    daily_medicine.router,
    prefix="/daily-medicines",
    tags=["Daily Medicines"],
    dependencies=[Depends(get_current_user)]
)

# DDID Database Routes (using AI database)
app.include_router(
    disease_information.router, 
    prefix="/ddid/disease-information", 
    tags=["DDID - Disease Information"], 
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    drug_information.router, 
    prefix="/ddid/drug-information", 
    tags=["DDID - Drug Information"], 
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    food_information.router, 
    prefix="/ddid/food-information", 
    tags=["DDID - Food Information"], 
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    herb_information.router, 
    prefix="/ddid/herb-information", 
    tags=["DDID - Herb Information"], 
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    drug_foodherb_interaction.router, 
    prefix="/ddid/interactions", 
    tags=["DDID - Drug-Food/Herb Interactions"], 
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    notification.router,
    prefix="/notifications",
    tags=["Notifications"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    user.router,
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)]
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <title>SenioCare</title>
    <div style="display:flex; flex-direction:column; align-items:center; margin-top:50px;">
      <h1 style="font-size:50px; font-family:'Brush Script MT', cursive;">
        #1
      </h1>
      <p style="font-size:20px; font-family:'Brush Script MT', cursive;">
        For more info please read the 
        <a href="/docs">docs</a>
      </p>
    </div>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=config.PORT, reload=True)
