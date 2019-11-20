import uvicorn
from fastapi import Header
from config import app, cur_connection, logger
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from model import UsersAddModel, UsersUpdateModel


def response_messages(result, success_status, errorCode):
    """
        This Function is used to generate the response message
    """
    message = {
        "errorCode": errorCode,
        "success": success_status,
        "result": result
    }
    return message


@app.post("/users/")
def add_users(users: UsersAddModel):
    """
        This API is used to add a employee
    """
    logger.info('USERS API-POST: INITIATED')
    try:
        json_compatible_data = jsonable_encoder(users)
        for user in json_compatible_data['userDetails']:
            cur_connection.execute("select * from employee where emp_email='" + user['email'] + "'")
            if cur_connection.rowcount > 0:
                logger.info('USERS API-POST: Employee Exists: %s', user['email'])
            else:
                values = (user['id'], user['name'], user['email'])
                cur_connection.execute("insert into employee values " + str(values))
                logger.info('USERS API-POST: Employee Added: %s', user['email'])
        message = response_messages([], True, "Employee Added Successfully..!!")
        return JSONResponse(content=message, status_code=201)
    except Exception as e:
        message = response_messages([], False, str(e))
        logger.error('USERS API-POST: Exception: ', str(e))
        return JSONResponse(content=message, status_code=500)


@app.get("/users/")
def users(offset: int = 0, limit: int = 10, emp_id: str = Header(None)):
    """
        This API is used to fetch all the users or a perticular user based on the emp_id passed in the Header
    """
    logger.info('USERS API-GET: INITIATED')
    try:
        users_list = []
        if emp_id:
            cur_connection.execute(
                "select * from employee where emp_id='" + emp_id + "'  limit " + str(limit) + " offset " + str(
                    offset) + ";")
        else:
            cur_connection.execute("select * from employee limit " + str(limit) + " offset " + str(offset) + ";")
        if cur_connection.rowcount > 0:
            for user in cur_connection:
                users_list.append({
                    "emp_id": user[0],
                    "emp_name": user[1],
                    "emp_email": user[2],
                })
            message = response_messages(users_list, True, "Success")
            logger.info('USERS API-GET: Success')
            return JSONResponse(content=message, status_code=200)
        else:
            message = response_messages(users_list, False, "No Data Found")
            logger.info('USERS API-GET: No Data Found')
            return JSONResponse(content=message, status_code=404)
    except Exception as e:
        message = response_messages([], False, str(e))
        logger.error('USERS API-GET: Exception: %s', str(e))

        return JSONResponse(content=message, status_code=500)


@app.patch("/user/")
def update_user(user: UsersUpdateModel, emp_id: str = Header(None)):
    """
        This API is used to update a employee details
    """
    logger.info('USERS API-PATCH: INITIATED')
    try:
        json_compatible_data = jsonable_encoder(user)
        cur_connection.execute("select * from employee where emp_id='" + emp_id + "'")
        if cur_connection.rowcount > 0:
            cur_connection.execute("update employee set emp_name='" + json_compatible_data['name'] + "', emp_email='" +
                                   json_compatible_data['email'] + "' where emp_id='" + emp_id + "'")
            message = response_messages([], True, "Employee Updated Successfully..!!")
            logger.info('USERS API-PATCH: Employee Updated Successfully: %s', emp_id)
            return JSONResponse(content=message, status_code=200)
        else:
            message = response_messages([], False, "No Data Found..!!")
            logger.info('USERS API-PATCH: No Data Found: %s', emp_id)
            return JSONResponse(content=message, status_code=404)
    except Exception as e:
        message = response_messages([], False, str(e))
        logger.error('USERS API-PATCH: Exception: %s', str(e))
        return JSONResponse(content=message, status_code=500)


@app.delete("/user/")
def delete_user(emp_id: str = Header(None)):
    """
        This API is used to delete a user based on the emp_id
    """
    logger.info('USER API-DELETE: INITIATED')
    try:
        cur_connection.execute("select * from employee where emp_id='" + emp_id + "'")
        if cur_connection.rowcount > 0:
            cur_connection.execute("delete from employee where emp_id='" + emp_id + "'")
            message = response_messages([], True, "Employee Deleted Successfully..!!")
            logger.info('USER API-DELETE: Employee Deleted Successfully: %s', emp_id)
            return JSONResponse(content=message, status_code=200)
        else:
            message = response_messages([], False, "No Data Found..!!")
            logger.info('USER API-DELETE: No Data Found: %s', emp_id)
            return JSONResponse(content=message, status_code=404)
    except Exception as e:
        message = response_messages([], False, str(e))
        logger.error('USER API-DELETE: Exception: %s', str(e))
        return JSONResponse(content=message, status_code=500)


if __name__ == "__main__":
    # Running the app as a server on 0.0.0.0:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
