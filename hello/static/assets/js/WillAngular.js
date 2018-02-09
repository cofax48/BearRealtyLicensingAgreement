//Functionalizes the App
var app = angular.module('app', [], function($httpProvider){
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller('Controller', function($scope, $http){
  //Initializes the List of BNB reviews for a particular bnb

  console.log('ayoooo');

  $scope.Credentials = function (Name, Address, Email, PhoneNum) {

    $scope.clientName = "../hello/static/images/pdfs/" + String(Name) + "pdf.pdf";
    console.log($scope);
    console.log(Name, Address, Email, PhoneNum);
    var post_upload = {
        "clientName" : Name,
        "Address" : Address,
        "Email" : Email,
        "PhoneNum" : PhoneNum
    }
    //Make a post call to the server/database to add a new user pdf
    $http.post('/pdfEdit', post_upload)
    .success(function(results) {
      console.log(results)
    });
  };


});
