# from fastapi import Depends, FastAPI, HTTPException
# from fastapi.responses import JSONResponse
# from sql_app import models
# from db import get_db, engine
# import sql_app.models as models
# import sql_app.schemas as schemas
# from sql_app.repositories import ItemRepo, StoreRepo
# from sqlalchemy.orm import Session
# import uvicorn
# from typing import List,Optional
# from fastapi.encoders import jsonable_encoder
#
#
# app = FastAPI(title="Base Pyaella Instance",
#     description="FastAPI Application with Swagger and Sqlalchemy for Pyaella",
#     version="0.0.1",)
#
#
# @app.exception_handler(Exception)
# def validation_exception_handler(request, err):
#     base_error_message = f"Failed to execute: {request.method}: {request.url}"
#     return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})
#
#
# @app.get('/pyaella-about')
# async def get_about():
#
#     return JSONResponse(title="Base Pyaella Instance",
#         description="FastAPI Application with Swagger and Sqlalchemy for Pyaella",
#         version="0.0.1",)

