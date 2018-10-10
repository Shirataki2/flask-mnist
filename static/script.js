(function () {
    const canvas = document.getElementById('mainCanvas');
    const ctx = canvas.getContext("2d");

    let defSize = 15;
    let defColor = "#ffffff";
    let mouseX = "";
    let mouseY = "";
    ctx.beginPath();
    ctx.fillStyle = "#000000";
    ctx.fillRect(0, 0, 500, 500);
    canvas.addEventListener('mousemove', onMove, false);
    canvas.addEventListener('touchmove', onMoveMob, false);
    canvas.addEventListener('mousedown', onClick, false);
    canvas.addEventListener('touchstart', onClickMob, false);
    canvas.addEventListener('mouseup', drawEnd, false);
    canvas.addEventListener('mouseout', drawEnd, false);
    canvas.addEventListener('touchend', drawEnd, false);
    canvas.addEventListener('touchcancel', drawEnd, false);

    function onMove(e) {
        if (e.buttons === 1 || e.witch === 1) {
            let rect = e.target.getBoundingClientRect();
            let X = ~~(e.clientX - rect.left);
            let Y = ~~(e.clientY - rect.top);
            draw(X, Y);
        }
    }

    function onMoveMob(e) {
        if (e.targetTouches.length == 1) {
            let touch = e.targetTouches[0];
            let rect = e.target.getBoundingClientRect();
            let X = ~~(touch.pageX - rect.left);
            let Y = ~~(touch.pageY - rect.top);
            draw(X, Y);
        }
    }

    function onClickMob(e) {
        if (e.targetTouches.length == 1) {
            let touch = e.targetTouches[0];
            let rect = e.target.getBoundingClientRect();
            let X = ~~(touch.pageX - rect.left);
            let Y = ~~(touch.pageY - rect.top);
            draw(X, Y);
        }
    }

    function onClick(e) {
        if (e.buttons === 0) {
            let rect = e.target.getBoundingClientRect();
            let X = ~~(e.clientX - rect.left);
            let Y = ~~(e.clientY - rect.top);
            draw(X, Y);
        }
    }

    function draw(X, Y) {
        ctx.beginPath();
        ctx.globalAlpha = 1.0;
        if (mouseX === "") {
            ctx.moveTo(X, Y);
        } else {
            ctx.moveTo(mouseX, mouseY);
        }
        ctx.lineTo(X, Y);
        ctx.lineCap = "round";
        ctx.lineWidth = defSize;
        ctx.strokeStyle = defColor;
        ctx.stroke();
        mouseX = X;
        mouseY = Y;
    }

    function drawEnd() {
        mouseX = "";
        mouseY = "";
    }

    let range = document.getElementById('lineWidth');
    let display = document.getElementById('width');
    let rangeValue = function (range, display) {
        return function (e) {
            display.innerHTML = range.value;
            defSize = range.value;
            console.log(ctx);
        }
    }
    range.addEventListener('input', rangeValue(range, display));

    let menuIcons = document.getElementsByClassName("drawMenu");
    for (let i = 0; i < menuIcons.length; i++){
        menuIcons[i].addEventListener("click", drawMenu, false);
        menuIcons[i].addEventListener("touchstart", drawMenu, false);
    }

    function drawMenu() {
        if (this.id.indexOf("draw") + 1) {
            defColor = "#ffffff";
        }
        if (this.id.indexOf("erase") + 1) {
            defColor = "#000000";
        }
        if (this.id.indexOf("clear") + 1) {
            if (confirm("すべて消去してもよろしいですか")) {
                ctx.beginPath();
                ctx.fillStyle = "#000000";
                ctx.fillRect(0, 0, 500, 500);
                defColor = "#ffffff";
            }
        }
    }

    function toImg(){
        let tmp = document.createElement('canvas');
        tmp.width = 500;
        tmp.height = 500;
        let tmpctx = tmp.getContext('2d');
        tmpctx.drawImage(canvas, 0, 0, 500, 500, 0, 0, 500, 500);
        let img = tmp.toDataURL('image/jpeg');
        return img;
    }

    $(".predict-btn").on('click', () => {
        $(".resultField").html('予測中...')
        let img = toImg();
        let dic = { img: img };
        $.ajax({
            url: "run",
            type: "POST",
            data: JSON.stringify(dic),
            success: function (dic) {
                console.log(dic)
            },
            error: function(e){
                console.log(e)
            },
            contentType: "application/json",
            dataType: 'json',
        }).done(function(data) {
            console.log("Successfully Image Posted");
            $(".resultField").html(`予測結果:${data['result']}`)
        }).error(function(data){
            console.log("Error Occured!");
            $(".resultField").html('結果の取得に失敗しました...')
        })
    });

    $(".predict-btn").on('touchstart', () => {
        $(".resultField").html('予測中...')
        let img = toImg();
        let dic = { img: img };
        $.ajax({
            url: "run",
            type: "POST",
            data: JSON.stringify(dic),
            success: function (dic) {
                console.log(dic)
            },
            error: function(e){
                console.log(e)
            },
            contentType: "application/json",
            dataType: 'json',
        }).done(function(data) {
            console.log("Successfully Image Posted");
            $(".resultField").html(`予測結果:${data['result']}`)
        }).error(function(data){
            console.log("Error Occured!");
            $(".resultField").html('結果の取得に失敗しました...')
        })
    });
})();