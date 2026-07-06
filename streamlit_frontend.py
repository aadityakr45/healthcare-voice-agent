#steps5:Streamlit Dashboard
import http
import streamlit as st
import datetime as dt
import requests


st.title("DPS Hospital Booking Portal")
base_url=st.text_input("Backend URL","http://127.0.0.1:4444").rstrip("/")

patient_name=st.text_input("Patient Name")
reason=st.text_input("Reason for Appointment")
start_date=st.date_input("Date",value=dt.date.today()+dt.timedelta(days=1))
start_time=st.time_input("Start Time",value=dt.time(hour=9,minute=0))

if st.button("Schedule"):
    start_dt=dt.datetime.combine(start_date,start_time)
    payload={
        "patient_name":patient_name.strip(),
        "reason":reason.strip(),
        "start_time":start_dt.isoformat(),
    }
    try:
        response=requests.post(f"{base_url}/schedule_appointment/",json=payload,timeout=10)
        if response.status_code==http.HTTPStatus.OK:
            st.success("Appointment Scheduled Successfully!")
        else:
            st.error(f"Failed to schedule appointment: {response.text}")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")



    
st.divider()
st.subheader("Cancel Appointments")

import time

    # Now refresh


cancel_name=st.text_input("pateint name",key="cancel_name")
cancel_date=st.date_input("Date to cancel",key="cancel_date",value=dt.date.today())

if st.button("Cancel appointments"):
    payload={
        "patient_name":cancel_name.strip(),
        "date":cancel_date.isoformat()
    }
    try:
        resp=requests.post(f"{base_url}/cancel_appointment/",json=payload,timeout=10)
        resp.raise_for_status()
        data=resp.json() if resp.content else {}
        #st.toast(f"Successfully cancelled {count} appointments!", icon="✅")
        st.success(f"Cancelled:{data.get('cancel_count',0)}")
        time.sleep(3)
        st.rerun()
    except requests.HTTPError:
        st.error(resp.text)
    except requests.RequestException as exc:
        st.error(f"Cancel Failed:{exc}")



appointments_date=st.date_input("date to check appointment",key="check_appointment_date",value=dt.date.today())
if st.button("Check appointments"):
    try:
        params={
            "date":appointments_date.isoformat()
        }
        resp=requests.get(f"{base_url}/list_appointments/",params=params,timeout=10)
        resp.raise_for_status()
        st.dataframe(resp.json(),use_container_width=True,hide_index=True)
    except requests.RequestException as exc:
        st.warning(f"Could not load appointments: {exc}")




    

