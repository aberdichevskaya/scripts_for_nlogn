function reRegisterOne(){
  var i = 2309
  reRegister(i, i)
}

function reRegisterSome(){
  reRegister(1967, 1975)
}

function reRegister(idxFrom, idxTo){

  try {
    const sheet = SpreadsheetApp.getActive().getSheetByName("Ответы на форму (1)").activate()
    const logins = SpreadsheetApp.getActive().getSheetByName("логины-пароли").activate()

    let connection = Jdbc.getConnection(db_url, db_user, db_password)

    const nameColumn = 2
    const loginColumn = 1
  
    var contestIDS = [220]


    for (var currentRow = idxFrom; currentRow <= idxTo; currentRow++){
      const name = sheet.getRange(currentRow, nameColumn, 1, 1).getValue()
      const login = logins.getRange(currentRow, loginColumn, 1, 1).getValue()

      if (login == "") throw "empty login"
      if (name == "") throw "empty name"

      for (var i = 0; i < contestIDS.length; i++){
        var contest_id = contestIDS[i]
      
        let results = connection.prepareStatement(
          'SELECT user_id FROM logins WHERE login="' + login + '"'
        ).executeQuery()
        results.first()
        let user_id = results.getInt(1)

        let deleteUserStmt = connection.prepareStatement(
          'DELETE FROM users WHERE user_id=? AND contest_id=?'
        )    
        deleteUserStmt.setInt(1, user_id)
        deleteUserStmt.setInt(2, contest_id)
        deleteUserStmt.execute()

        let insertUsersStmt = connection.prepareStatement(
          'INSERT INTO users(user_id, contest_id, username) VALUES(?, ?, ?)'
        )
        insertUsersStmt.setString(1, user_id)
        insertUsersStmt.setString(2, contest_id)
        insertUsersStmt.setString(3, name)
        insertUsersStmt.execute()
      }
    }
    return true
  }
  catch (err) {
    Logger.log("Bad Stuff")
    return true
  }
}
