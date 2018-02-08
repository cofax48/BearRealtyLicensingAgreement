//Functionalizes the App
var app = angular.module('app', [], function($httpProvider){
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller('Controller', function($scope, $http){
  //Initializes the List of BNB reviews for a particular bnb

  console.log('ayoooo');

  $scope.Credentials = function (Name, Address, Email, PhoneNum) {

    $scope.clientName = "../static/images/pdfs/" + String(Name) + "pdf.pdf";
    console.log($scope);
    console.log(Name, Address, Email, PhoneNum);
    var post_upload = {
        "clientName" : Name,
        "Address" : Address,
        "Email" : Email,
        "PhoneNum" : PhoneNum
    }
    //Make a post call to the server/database to add a new user db table
    $http.post('/pdfEdit', post_upload)
    .success(function(results) {
      console.log(results)
    });
  };




  /*
  $scope.BNBList = [];

  //Initializes the list of all bnb's that have been reviewed
  $scope.BNBReviewList = [];

  $scope.PreviousUserReviewsList = [];

  //Sends the new usr name to the db
  $scope.newUsers = function newUsers (userNames) {
    $scope.currentUser = userNames;
    var post_upload = {
        "user" : "Josh_Schenkein",
        "title" : "Great Place for a swim",
        "description" : "never had a better stay",
        "expiration" : "2017-12-1712:55:48",
        "location" :
        {
            "x" : 846739726,
            "y" : 93762524417
        }
    }
    //Make a post call to the server/database to add a new user db table
    $http.post('/api/listings/add_new_listing', post_upload)
    .success(function(results) {
      console.log(results)
    }).
    error(function(error) {
      console.log(error)
    });

    //Shows fields now that sign in has occurred
    d3.select("form#existingBNB")
      .style("visibility", "visible");
    //Hides returningUser
    d3.select("form#returninguser")
      .style("visibility", "hidden");
    //Allows for new review to be added
    d3.select("form#addNewReview")
      .style("visibility", "visible");
    d3.select("form#addNewBNB")
      .style("visibility", "visible");
  };

  //Gts existing users reviews
  $scope.returningUser = function returningUser (userName) {
    $scope.currentUser = userName;
    //Get all todos for user and is fired after user signs in
    $http.post('api/get_user', {"userName":userName})
    .then(function (response) {
      console.log(response);
      response.data.data.forEach(function(review){
        console.log(review);
        //pushes th response from th api call to th scope to update th view
        $scope.PreviousUserReviewsList.push({"userName":userName, "bnb":review[2], "review":review[1], "timestamp":unixTimeStampConverter(review[0])});
      });//Forach in list
    })//Then
    .catch(function (response) {
        console.error('API error', response.status, response.data);
    })
    .finally(function () {
      console.log('data uploaded');
    });

    //Shows fields now that sign in has occurred
    d3.select("form#existingBNB")
      .style("visibility", "visible");
    //Hides newUser
    d3.select("form#newuser")
      .style("visibility", "hidden");
    //Allows for new review to be added
    d3.select("form#addNewReview")
      .style("visibility", "visible");
    d3.select("form#addNewBNB")
      .style("visibility", "visible");
  };

  //gets previously authored reviews from db
  $scope.existingBNBSelected = function existingBNBSelected(BNBSelected) {
    console.log(BNBSelected);
    //cycles through the list of bnb names and when they match with chosen
    //bnb, the chosen bnb api fired
    var BNBChosen = [];
    $scope.BNBReviewList.forEach(function(bnbName) {
      bnbName = bnbName.replace(/.$/,"") //had an issue with trailing whitespace
      if (bnbName == BNBSelected) {
        BNBChosen.push(BNBSelected);
        $scope.currentBNB = BNBSelected;
      };
    });

    if (BNBChosen.length > 0) {
      $http.post('/api/get_review', {"bnb":BNBChosen[0]})
      .then(function (response) {
        response.data.data.forEach(function(review){
          console.log(review);
          //pushes th response from th api call to th scope to update th view
          $scope.BNBList.push({"userName":review[2], "review":review[1], "bnb":BNBChosen[0], "timestamp":unixTimeStampConverter(review[0])});
        });//Forach in list
      })//Then
      .catch(function (response) {
          console.error('API error', response.status, response.data);
      })
      .finally(function () {
        console.log('data uploaded');
      });
    };
  };

  //Adds a new bnb
  $scope.AddANewBNB = function AddANewBNB (newReview, newBNB) {
    $scope.currentBNB = newBNB;
    //Make a post call to the server/database for a new bnb
    $http.post('api/add_bnb', {"userName":$scope.currentUser, "bnb":newBNB, "review":newReview})
    .success(function(results) {
      console.log('yayyy')
    }).
    error(function(error) {
      console.log(error)
    });

    var now = new Date().toLocaleString();
    $scope.BNBList.push({"userName":$scope.currentUser, "bnb":$scope.currentBNB, "review":newReview, "timestamp":now});
    $scope.PreviousUserReviewsList.push({"userName":$scope.currentUser, "bnb":$scope.currentBNB, "review":newReview, "timestamp":now});

    //calls the function which populates bnb list
    getBNBLIst();
  };


  //Adds a new review
  $scope.AddANewReview = function AddANewReview (newReview) {
    var now = new Date().toLocaleString();
    $scope.BNBList.push({"userName":$scope.currentUser, "bnb":$scope.currentBNB, "review":newReview, "timestamp":now});
    $scope.PreviousUserReviewsList.push({"userName":$scope.currentUser, "bnb":$scope.currentBNB, "review":newReview, "timestamp":now});
    //Make a post call to the server/database for a new word
    $http.post('api/add_review', {"userName":$scope.currentUser, "bnb":$scope.currentBNB, "review":newReview})
    .success(function(results) {
      console.log('yayyy')
    }).
    error(function(error) {
      console.log(error)
    });
  };

  //Gts existing reviews by destination
  $scope.existingBNB = function existingBNB (BNB) {
    $scope.currentBNB = BNB;
    //Get all todos for user and is fired after user signs in
    $http.post('api/get_review', {"bnb":BNB})
    .then(function (response) {
      response.data.data.forEach(function(review){
        console.log(review);
        //pushes th response from th api call to th scope to update th view
        $scope.BNBList.push({"userName":review[2], "review":review[1], "bnb":BNB, "timestamp":unixTimeStampConverter(review[0])});
      });//Forach in list
    })//Then
    .catch(function (response) {
        console.error('API error', response.status, response.data);
    })
    .finally(function () {
      console.log('data uploaded');
    });
  };

  $scope.wordListRemoval = [];
  $scope.selectedWords = function selectedWords(word) {
    $scope.wordListRemoval.push(word);
    console.log(word);
  }

  $scope.remove = function remove() {
    var oldList = $scope.WordList;
    $scope.WordList = [];
    $scope.wordListRemoval.forEach(function(word) {
      $http.post('/api/delete_word', {"userName": $scope.currentUser, "wordToDelete":word["Word"]})
      .success(function(results) {
        console.log('yayyy')
        //copy the old list-remove deleted item and push old list minus deleted item back to scope
        oldList.forEach(function(wordItem) {
          console.log(wordItem);
          if (wordItem["Word"] != word["Word"]) {
            $scope.WordList.push(wordItem);
          };//if
        });//Oldlist loop

      }).
      error(function(error) {
        console.log(error)
      });
    });
  };

  //Hides fields until sign in
  d3.select("form#existingBNB")
    .style("visibility", "hidden");
  d3.select("div#removeButton")
    .style("visibility", "hidden");
  d3.select("form#addNewReview")
    .style("visibility", "hidden");
  d3.select("form#addNewBNB")
    .style("visibility", "hidden");

  function getBNBLIst() {
    //populates datalist of previously reviewed bnbs on load
    $http.post('/api/get_bnb')
    .then(function (response) {
      response.data.data.forEach(function(bnb){
        //pushes th response from th api call (aka list of bnbs) to th datalist
        $scope.BNBReviewList.push(bnb);
      });//Forach in list
    })//Then
    .catch(function (response) {
        console.error('API error', response.status, response.data);
    })
    .finally(function () {
      console.log('data uploaded');
    });
  };

  function unixTimeStampConverter(unix_timestamp) {
    var a = new Date(unix_timestamp * 1000);
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = a.getDate();
    var hour = a.getHours();
    var min = a.getMinutes();
    var sec = a.getSeconds();
    var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
    return time;
  }

  getBNBLIst();

  */

});
