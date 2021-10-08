import mysql.connector

def task7():
  # ssh -L 3306:groucho.it.uu.se:3306 -o TCPKeepAlive=yes -o ServerAliveInterval=10 ID@beurling.it.uu.se
  mysqlconnect()
  if (mydb.is_connected()):
    print("Connected")
  else:
    print("Not connected")
  main_menu()
  mydb.close()

def mysqlconnect():
  global mydb
  mydb = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="ht21_1_group_19",
    passwd="pwd_19",
    database="ht21_1_project_group_19",
    auth_plugin='mysql_native_password'
  )
  global mycursor
  mycursor = mydb.cursor()

def main_menu():
  val=0

  EXIT = -1
  DEPT_ID  = 1
  PROD_ID  = 2
  CONTINUE = 0
  val = CONTINUE

  while(val != EXIT):

    # ACCEPT USER INPUT. WRAP IN TRY/CATCH FOR BAD USER INPUT
    try:
      val = int(input(f"Enter {DEPT_ID} for Department ID. Enter {PROD_ID} for Product ID. Enter {EXIT} to exit: "))
    except:
      val = CONTINUE
    
    if (val == DEPT_ID):
      dept_id()
    elif (val ==PROD_ID):
      prod_id()
    elif (val == EXIT):
      print("Bye!")
      break

def dept_id():
  EXIT = -1
  VIEWALL  = -2
  CONTINUE = -3
  val = CONTINUE
  inputval = ""

  while(val != EXIT):
    
    # ACCEPT USER INPUT. WRAP IN TRY/CATCH FOR BAD USER INPUT
    try:
      inputval = input(f"\nEnter the Department ID to view department. Enter {VIEWALL} to view all deptarments. Enter {EXIT} to exit: ")
      val = int(inputval)
    except:
      val = CONTINUE

    # RETURN TO MAIN MENU
    if (val == EXIT):
      break

    # PRINT ALL AVAILABLE DEPARTMENTS
    elif (val == VIEWALL):
      mycursor.execute("SELECT Dept_ID, Title FROM Department;")
      myresult = mycursor.fetchall()
      for x in myresult:
        print(x)
      continue
    else:

      # CHECK DEPT EXISTS
      mycursor.execute(f"SELECT EXISTS(SELECT * FROM Department WHERE Dept_ID = {val});")
      myresult = mycursor.fetchall()
      dept_exist = bool(myresult[0][0])

      # THE DEPT EXISTS
      if(dept_exist):
        # Is it a leaf department?
        mycursor.execute(f"SELECT * FROM Department WHERE Sup_Dep = {val};")
        myresult = mycursor.fetchall()
        result_len = len(myresult)
        is_leaf = not bool(result_len)

        # SHOW PRODUCTS
        if(is_leaf):
          mycursor.execute(f"SELECT Product_ID, Title, Price * (1-Discount) * (1+Tax) FROM Products WHERE Dept_ID = {val};")
          myresult = mycursor.fetchall()
          print(f"\nDepartment {val} is a leaf node. Here are the products:")
          for x in myresult:
            print(x)

        # SHOW SUBDEPARTMENTS
        else:
          mycursor.execute(f"SELECT * FROM Department WHERE Sup_Dep = {val};")
          myresult = mycursor.fetchall()
          print(f"\nDepartment {val} is not a leaf node. Here are the subdepartments:")
          for x in myresult:
            print(x)

      # THE DEPT DOES NOT EXIST
      else:
        print(f"Department {inputval} does not exist. Try again.")

def prod_id():
  print("prod id")
  EXIT = -1
  VIEWALL  = -2
  CONTINUE = -3
  val = CONTINUE
  inputval = ""

  while(val != EXIT):
    
    # ACCEPT USER INPUT. WRAP IN TRY/CATCH FOR BAD USER INPUT
    try:
      inputval = input(f"\nEnter the Product ID to view a product's discount. Enter {VIEWALL} to view all products. Enter {EXIT} to exit: ")
      val = int(inputval)
    except:
      val = CONTINUE

    # RETURN TO MAIN MENU
    if (val == EXIT):
      break

    # PRINT ALL AVAILABLE DEPARTMENTS
    elif (val == VIEWALL):
      mycursor.execute("SELECT Product_ID, Title, Discount FROM Products;")
      myresult = mycursor.fetchall()
      for x in myresult:
        print(x)
      continue
    else:

      # CHECK PROD EXISTS
      mycursor.execute(f"SELECT EXISTS(SELECT * FROM Products WHERE Product_ID = {val});")
      myresult = mycursor.fetchall()
      prod_exist = bool(myresult[0][0])

      # THE PROD EXISTS
      if(prod_exist):
        mycursor.execute(f"SELECT Product_ID, Title, Discount FROM Products WHERE Product_ID = {val};")
        myresult = mycursor.fetchall()
        for x in myresult:
          print(x)
        prod_id = val
        try:
          inputval = input(f"\nEnter a new discount using decimal format (ie enter .07 for a 7% discount) in the range [0,1): ")
          val = float(inputval)
          if val < 0:
            val = 0
          elif val >=1:
            val = .99
          mycursor.execute(f"Update Products SET Discount = {val} WHERE Product_ID = {prod_id} ;")
          mycursor.execute(f"SELECT Product_ID, Title, Discount FROM Products WHERE Product_ID = {prod_id};")
          myresult = mycursor.fetchall()
          for x in myresult:
            print(x)
        except:
          continue

      # THE DEPT DOES NOT EXIST
      else:
        print(f"Product ID {inputval} does not exist. Try again.")

task7()