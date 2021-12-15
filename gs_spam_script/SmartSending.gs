
function processLastWithSmartSending(email) {
  const sheet = SpreadsheetApp.getActive().getSheetByName("Ответы на форму (1)").activate()
  var last_row = sheet.getLastRow()
  if (is_good_mail(email) == false) return
  processEjudge(last_row)
}

function is_good_mail(email){
  var num_rest = MailApp.getRemainingDailyQuota();
  let connection = Jdbc.getConnection(db_url, db_user, db_password)

  res = connection.createStatement().executeQuery('SELECT email FROM cognitive_2021_mails ORDER BY num DESC LIMIT 1;')
  res.next()
  biggest = res.getString(1)

  if (biggest == email) {
    Logger.log("USING THIS ONE")

    connection.close()
    Utilities.sleep(10000) // so other threads can read from database. Now there should not be any collisions
    connection = Jdbc.getConnection(db_url, db_user, db_password)

    let delete_query = connection.prepareStatement('DELETE FROM cognitive_2021_mails WHERE email=?;')
    delete_query.setString(1, email)
    delete_query.execute();

    let insert_query = connection.prepareStatement('INSERT INTO cognitive_2021_mails(email, num) VALUES(?, ?);')
    insert_query.setString(1, email)
    insert_query.setInt(2, num_rest)
    insert_query.execute()
  }
  else {
    Logger.log("other is better")
  }

  Logger.log("current: " + email)
  Logger.log("biggest: " + biggest)
  
  if (biggest == email) return true
  return false
}

function getEmailsTable(){
  let connection = Jdbc.getConnection(db_url, db_user, db_password)
  table = connection.createStatement().executeQuery('SELECT * FROM cognitive_2021_mails ORDER BY num DESC;')
  while(table.next()) {
    Logger.log(table.getString(1) + " " + table.getInt(2))    
  }
}

function deleteMailFromTable(){
  email = "theregoesnothing"
  connection = Jdbc.getConnection(db_url, db_user, db_password)
  let delete_query = connection.prepareStatement('DELETE FROM cognitive_2021_mails WHERE email=?;')
  delete_query.setString(1, email)
  delete_query.execute();
  getEmailsTable()
}

function processLastSmart_prognlogn() { return processLastWithSmartSending("prognlogn") }
function processLastSmart_nlognprog() { return processLastWithSmartSending("nlognprog") }
function processLastSmart_theregoesnothing() { return processLastWithSmartSending("theregoesnothing") }






