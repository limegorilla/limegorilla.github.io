// JavaScript Document

$(function(){
  $("#menu").css("display","none");

  $("#menutoggle").click(function(){
    $("#menu").slideToggle(100);
	  $("#menu-logo").toggle(); 
  })  
})

$("#menu-about").hover(function(){
  $("body").css("background-color", "#FF58EE");
  }, function(){
  $("body").css("background-color", "#3A3A3A");
});

$("#menu-portfolio").hover(function(){
  $("body").css("background-color", "#7E58FF");
  }, function(){
  $("body").css("background-color", "#3A3A3A");
});

$("#menu-projects").hover(function(){
  $("body").css("background-color", "#58E2FF");
  }, function(){
  $("body").css("background-color", "#3A3A3A");
});

$("#menu-contact").hover(function(){
  $("body").css("background-color", "#FF8843");
  }, function(){
  $("body").css("background-color", "#3A3A3A");
});