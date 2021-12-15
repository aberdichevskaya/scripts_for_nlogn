
function ProcessOne() {
  var x = 2334
  processRange(x, x)
}

function ProcessSome(){
  processRange(2339, 2341)
}

function processRange(a, b){
  for (var i = a; i <= b; i++) {
    processEjudge(i, false);
    Logger.log(i);
  }
}

function processLast(){
  const sheet = SpreadsheetApp.getActive().getSheetByName("Ответы на форму (1)").activate()
  processEjudge(sheet.getLastRow());
}

function processEjudge(currentRow) {

  const sheet = SpreadsheetApp.getActive().getSheetByName("Ответы на форму (1)").activate()
  const logins = SpreadsheetApp.getActive().getSheetByName("логины-пароли").activate()

  const nameColumn = 2
  const emailColumn = 4
  
  const loginColumn = 1
  const passwordColumn = 2
  
  const name = sheet.getRange(currentRow, nameColumn, 1, 1).getValue()
  const email = sheet.getRange(currentRow, emailColumn, 1, 1).getValue()

  const login = logins.getRange(currentRow, loginColumn, 1, 1).getValue()
  const password = logins.getRange(currentRow, passwordColumn, 1, 1).getValue()

  if (login == "") throw "empty login"
  if (password == "") throw "empty password"
  if (name == "") throw "empty name"
  
  logins.getRange(currentRow, 3, 1, 1).setValue(name)
  logins.getRange(currentRow, 4, 1, 1).setValue(email)

  if (reRegister(currentRow, currentRow)) {
  //if (createUserEjudge(currentRow)) {
    send_seccess_mail(login, password, name, email)
    logins.getRange(currentRow, 5, 1, 1).setValue("письмо успешно отправлено")
  } else {
    Logger.log("Fail")
    //send_failure_mail(name, email)
    //logins.getRange(currentRow, 5, 1, 1).setValue("ошибка при регистрации")
  }
}

const db_server = "ejudge.nlogn.info"
const db_name = "ejudge"
const db_port = 3306

const db_url = 'jdbc:mysql://' + db_server + ":" + db_port + "/" + db_name + "?useUnicode=yes&characterEncoding=UTF-8"
const db_user = "ejudge"
const db_password = "ejudge"


// Connects to Ejudge database and inserts new user info
function createUserEjudge(currentRow) {
  return reRegister(currentRow, currentRow)
}



function send_seccess_mail(login, password, name, email) {

  var subject = "Поздравляем с успешной регистрацией"

  var body = "Привет, " + name + "!<br \/>" +
  "Поздравляем с успешной регистрацией на олимпиаду \"Когнитивные технологии\".<br \/><br \/>" +
"Отборочный тур олимпиады \"Когнитивные Технологии\" стартует 10 декабря в 10:00 и продлится до 23:59 19 декабря (время московское).<br \/><br \/>" +
"Контест проходит на тестирующей системе ejudge. Данные для входа:<br \/>" + 
"Логин -  " + login + "<br \/>" +
"Пароль - " + password + "<br \/><br \/>" +
"Ссылка на контест: http://ejudge.misis.ru/cgi-bin/new-client?contest_id=220.<br \/><br \/>" +   
"Контест виртуальный - это значит, что начать его можно в любой момент в период во время отборочного тура. После старта у вас будет 4 часа на решение задач. Внимание! После старта контест нельзя поставить на паузу.<br \/><br \/>" +  
"Рекомендуем сначала написать пробный тур. Для этого заполните форму https://docs.google.com/forms/d/e/1FAIpQLSf4LhKj6S0Sv0bEhKJf3ZuCYUrMKa-s2cpAkSZG949XfnYSPw/viewform и дождитесь письма со ссылкой на контест и данными для входа в систему.<br \/><br \/>" + 
"Также на сайте олимпиады olymp.misis.ru вы найдете видео,  которые помогут вам познакомиться с форматом олимпиады и с решениями задач из пробного тура.<br \/><br \/>" + 
"Ссылка на организационный чат: https://t.me/joinchat/7PpgtwTsVK4xMDE6. В нём мы ответим на ваши вопросы по проведению олимпиады. Внимание! Обсуждать решение задач в чате строго запрещено.<br \/><br \/>" +
"Также по организационным вопросам можно писать в телеграм @olympcognitive.<br \/><br \/>" +

"Ссылка на паблик организаторов, где мы будем публиковать новости олимпиады и не только: https://vk.com/acmmisis.<br \/><br \/>" +
"Желаем удачи!"

  MailApp.sendEmail({to: email, subject: subject, htmlBody: body, name: "Олимпиада \"Когнитивные технологии\""})
  Logger.log("Done")
}


function send_failure_mail(name, email) {
  var body = "Привет, " + name + "!<br \/>" +
        "Произошла какая-то ошибка.<br \/>" +
        "Обратись к организаторам по почте support@nlogn.info либо в телеграм @olympcognitive.<br \/>"

  MailApp.sendEmail({
        to: email, 
        subject: "Ошибка при регистрации на олимпиаду \"Когнитивные Технологии\"", 
        htmlBody: body, 
        name: "Олимпиада Когнитивные технологии"})
}
