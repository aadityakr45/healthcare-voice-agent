#steps1:import database objects
#steps2:Create fastAPI endpoints for CRUD operations on the database objects
#steps3:Create Data Contracts (pydantic)
#steps4:Write Main Code
# #steps5:Streamlit Dashboard


import datetime as dt
import dateutil
from dateutil import parser
#steps1:import database objects
from database import init_db,Appointment
from sqlalchemy.orm import Session
init_db()

#steps3:Create Data Contracts (pydantic)
from pydantic import BaseModel, Field
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional

class AppointmentRequest(BaseModel):
    # validation_alias allows it to work even if Vapi sends "pateint_name" by mistake
    patient_name: str = Field(..., validation_alias="patient_name") 
    reason: str
    start_time: str # Receive as string first to prevent 422 validation errors

    @field_validator('start_time')
    def parse_datetime(cls, v):
        try:
            # Cleans up ISO strings Vapi might send (like '2026-02-20T10:30Z')
            return dt.datetime.fromisoformat(v.replace('Z', ''))
        except (ValueError, TypeError):
            raise ValueError("Invalid date format. Use YYYY-MM-DDTHH:MM:SS")

    model_config = ConfigDict(populate_by_name=True) # Allows both name and alias
#class AppointmentRequest(BaseModel):
 #   patient_name: str=Field(...)
 #   reason: str=Field(... )
 #   start_time: dt.datetime

class AppointmentResponse(BaseModel):
    id: int
    patient_name: str
    reason: str
    start_time: dt.datetime
    cancelled: bool
    created_at: dt.datetime
    class Config:
        from_attributes = True

class CancelAppointmentRequest(BaseModel):
    patient_name: str=Field(...)
    date: dt.datetime

class CancelAppointmentResponse(BaseModel):
    cancel_count:int


class ListAppointmentRequest(BaseModel):
    date: str = Field(..., description="The date spoken by the user")


#steps2:Create fastAPI endpoints for CRUD operations on the database objects
from fastapi import FastAPI,HTTPException,Depends
from database import get_db
app=FastAPI()
#schedule appt endpoint
@app.post("/schedule_appointment/")
def schedule_appointment(request:AppointmentRequest,db:Session=Depends(get_db)):
    new_appointment=Appointment(
        patient_name=request.patient_name,
        reason=request.reason,
        start_time=request.start_time
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    new_appointment_return_obj=AppointmentResponse(
        id=new_appointment.id,
        patient_name=new_appointment.patient_name,
        reason=new_appointment.reason,
        start_time=new_appointment.start_time,
        cancelled=new_appointment.cancelled,
        created_at=new_appointment.created_at
    )
    return new_appointment_return_obj

#cancel appt endpoint
from sqlalchemy import select
@app.post("/cancel_appointment/")
def cancel_appointment(request:CancelAppointmentRequest,db:Session=Depends(get_db)):
    start_dt=dt.datetime.combine(request.date,dt.time.min)
    end_dt=start_dt+dt.timedelta(days=1)

    result=db.execute(
        select(Appointment)
        .where(Appointment.patient_name==request.patient_name)
        .where(Appointment.start_time>=start_dt)
        .where(Appointment.start_time<end_dt)
        .where(Appointment.cancelled==False)
    )
    appointments=result.scalars().all()
    if not appointments:
        return HTTPException(status_code=404,detail="no appointment matching found ")
    for appointment in appointments:
        appointment.cancelled=True
    
    db.commit()
    return CancelAppointmentResponse(cancel_count=len(appointments))


#this below is for streamlit to show list of data

"""@app.get("/list_appointments/", response_model=list[AppointmentResponse])
def list_appointments(date: dt.date, db: Session = Depends(get_db)):
    start_dt = dt.datetime.combine(date, dt.time.min)
    end_dt = start_dt + dt.timedelta(days=1)
    
    # 1. Use .scalars() to get the actual Appointment objects
    result = db.execute(
        select(Appointment)
        .where(Appointment.cancelled == False)
        .where(Appointment.start_time >= start_dt)
        .where(Appointment.start_time < end_dt)
        .order_by(Appointment.start_time.asc())
    ).scalars().all() # <--- Added .scalars().all()

    booked_appointments = []
    for appointment in result:
        # Now 'appointment' is the actual model instance
        appointment_obj = AppointmentResponse(
            id=appointment.id,
            patient_name=appointment.patient_name,
            reason=appointment.reason,
            start_time=appointment.start_time,
            cancelled=appointment.cancelled,
            created_at=appointment.created_at
        )
        booked_appointments.append(appointment_obj)
        
    return booked_appointments"""

@app.post("/list_appointments/", response_model=list[AppointmentResponse])
def list_appointments(request: ListAppointmentRequest, db: Session = Depends(get_db)):
    try:
        # 2. CONVERT STRING TO DATE: 
        # This turns "Feb 20th" or "tomorrow" into a real Python date object
        parsed_date = parser.parse(request.date, fuzzy=True).date()
    except Exception:
        # If the date is complete gibberish, return an empty list or error
        return []

    # 3. YOUR ORIGINAL LOGIC (Now using parsed_date)
    start_dt = dt.datetime.combine(parsed_date, dt.time.min)
    end_dt = start_dt + dt.timedelta(days=1)
    
    result = db.execute(
        select(Appointment)
        .where(Appointment.cancelled == False)
        .where(Appointment.start_time >= start_dt)
        .where(Appointment.start_time < end_dt)
        .order_by(Appointment.start_time.asc())
    ).scalars().all()

    # 4. CLEANER RETURN:
    # FastAPI can automatically convert the list of DB objects if 
    # your AppointmentResponse has 'from_attributes = True'
    return result


import uvicorn
if __name__=="__main__":
    uvicorn.run("backend:app",host="127.0.0.1",port=4444,reload=True)


#steps4:Write Main Code

#steps5:Streamlit Dashboard
