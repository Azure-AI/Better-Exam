let exam_json = {
    "exam": {
        "title": "",
        "email": "",
        "questions": []
    }
};
let qnumber = 0;

function set_email() {
    var form1 = document.getElementById("form1");
    console.log(form1);
    document.getElementById("card2").style.display = "flex";
    document.getElementById("card1").style.display = "none";

}

function add_MC_question() {
    qnumber++;
    $("#question_area").append(`<div id="MC" name="question" class="form-group" style="text-align:left; border: 1px lightgray solid; padding: 5px">
                        <label>Multiple Choice Question - <a onclick="remove_element(this.parentElement.parentElement)"> Remove</a></label>
                        <textarea rows="2" class="form-control" required></textarea>
                        <label>A.</label>
                        <input type="text" class="form-control" required>
                        <label>B.</label>
                        <input type="text" class="form-control" required>
                        <label>C.</label>
                        <input type="text" class="form-control" >
                        <label>D.</label>
                        <input type="text" class="form-control" >
                    </div>`)
}

function add_ES_question() {
    qnumber++;
    $("#question_area").append(`<div id="ES" name="question" class="form-group" style="text-align:left; border: 1px lightgray solid; padding: 5px">
                            <label for="email">Essay Question - <a onclick="remove_element(this.parentElement.parentElement)"> Remove</a></label>
                            <textarea rows="4" class="form-control" required></textarea>
                        </div>`)
}

function remove_element(elm) {
    qnumber--;
    elm.remove();
}

function submit_exam() {
    let questions = document.getElementsByName("question");
    let qnumber = 0;
    exam_json['exam']['title'] = document.getElementById("exam_title").value
    questions.forEach(function (question) {
        qnumber++;
        if (question.id == "MC") {
            let MC_question = {
                "number": `${qnumber}`,
                "type": "MC",
                "text": question.childNodes[3].value,
                "choices": [
                    {"letter": "A", "text": question.childNodes[7].value}, {
                        "letter": "B",
                        "text": question.childNodes[11].value
                    }, {"letter": "C", "text": question.childNodes[15].value}, {
                        "letter": "D",
                        "text": question.childNodes[19].value
                    }
                ],
                "answer": ""
            };
            exam_json['exam']['questions'].push(MC_question);
            // console.log(MC_question)
        } else if (question.id == "ES") {
            let ES_question = {
                "number": `${qnumber}`,
                "type": "ES",
                "text": question.childNodes[3].value,
                "answer": ""
            };
            exam_json['exam']['questions'].push(ES_question);
        }
    });
    console.log(exam_json);
    let data = JSON.stringify(exam_json);
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            console.log(this.responseText);
        }
    });

    xhr.open("POST", "http://localhost:5000/exam/answer");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.send(data);
}