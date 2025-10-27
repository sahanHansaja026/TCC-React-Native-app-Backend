from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas

router = APIRouter()

@router.get("/get_parking_locations")
def get_parking_locations(db: Session = Depends(get_db)):
    parking_lots = db.query(models.ParkingLot).filter(
        models.ParkingLot.latitude.isnot(None),
        models.ParkingLot.longitude.isnot(None)
    ).all()

    return [
        {
            "parkinglotid": lot.parkinglotid,
            "lotname": lot.lotname,
            "location": lot.location,
            "lat": float(lot.latitude),
            "lng": float(lot.longitude)
        }
        for lot in parking_lots
    ]


@router.get("/get_map_locations")
def get_map_locations(db: Session = Depends(get_db)):
    parking_lots = db.query(models.ParkingLot).filter(
        models.ParkingLot.latitude.isnot(None),
        models.ParkingLot.longitude.isnot(None)
    ).all()

    return [
        {"lat": lot.latitude, "lng": lot.longitude}
        for lot in parking_lots
    ]
