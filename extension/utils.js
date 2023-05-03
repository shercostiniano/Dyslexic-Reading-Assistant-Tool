function getStoryData(){
    var textElements = document.querySelectorAll('div.bookreading_content__textArea__dqYNj');
    var imageElements = document.querySelectorAll('div.bookreading_content__imageArea__2IfX3');

    var resultArray = {};

    for (var i = 0; i < textElements.length; i++) {
        resultArray[i] = {"textArea": '', "imageArea": ''};
        resultArray[i].textArea = textElements[i].textContent;
        
        var img = imageElements[i].querySelector('img');
        if (img) {
            resultArray[i].imageArea = img.src;
        }
    }

    return resultArray;
}