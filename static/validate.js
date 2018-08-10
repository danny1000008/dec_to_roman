function clickRadioButton() {
  if (document.getElementById("decimal").checked) {
    document.getElementById("startValue").placeholder = "ex: 1950";
    document.getElementById("startValueTip").innerHTML = "must be between 1 and 4999";
  } else {
    document.getElementById("startValue").placeholder = "ex: MCML";
    document.getElementById("startValueTip").innerHTML = "must be a string of characters from the set {I, V, X, L, C, D, M}";
  }
}

function validateForm() {
  let formValue = document.forms["mainForm"]["numType"].value;
  let initialValue = document.forms["mainForm"]["startValue"].value;
  if (formValue == "decimal") {
    let re = /[^0-9]+/;
    if (initialValue == "" || re.test(initialValue) ||
      parseInt(initialValue) <= 0 || parseInt(initialValue) >= 5000) {
      alert("Enter an integer between 1 and 4999");
      return false;
    } else {
      console.log(formValue + ", " + initialValue)
      return true;
    }
  } else { // formValue == roman
    let re = /[^IVXLCMD]+/;
    if (re.test(initialValue.toUpperCase())) {
      alert("Enter an roman numeral (make sure to use only upper case letters)");
      return false;
    } else {
      return true;
    }
  }
}
