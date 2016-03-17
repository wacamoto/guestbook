itemList = function() {
    this.data;
    this.itemBox = $('#commentItem')
    var html = '<div class="item">\
                    <div class="middle aligned content">\
                        <a class="header" href="showboard?board_id={0}">{1}</a>\
                        <div class="extra">\
                            <div class="ui right floated button boardDeleteBtn" id="{0}">Delete</div>\
                        </div>\
                    </div>\
                </div>'

    this.updateUi = function() {
        var content = '';

        for (i in this.data) {
            var item = html;
            item = item.format(
                this.data[i].id, 
                this.data[i].pageurl
            )
            content += item
        }
        this.itemBox.html(content)
    }
    this.updateData = function() {
        this.data = (function() {
            var temp = 'XD';
            $.ajax({
                'async': false,
                'dataType': "json",
                'url': 'board',
                'success': function (data) {
                    temp = data;
                }
            });
            return temp; 
        })()
        
    }
    this.update = function() {
        this.updateData()
        this.updateUi()
    }
}

$(document).ready(function(){
    
    if ($('#commentItem').length){
        boardList = new itemList()
        boardList.update()

        $('#createBoardForm').submit(function(e){
            var url = $('#newBoardVal').val()
            $.ajax({
                url: 'board',
                type: 'POST',
                dataType: 'json',
                data: {board_url: url}
            }).done(function(data){
                alert(data)
            })
            e.preventDefault();
            boardList.update()
        })

        $('#commentItem').on('click', '.boardDeleteBtn', function(e){
            $.ajax({
                url: 'board?board_id=' + $(this).attr('id'),
                type: 'DELETE',
                dataType: 'json',
                success: function(data) {
                    alert(data)
                    boardList.update()
                }
            })
            console.log('board?board_id=' + $(this).attr('id'))
        })
        
    } else {
        $('#loginForm').submit(function(e){
            var usermailval = $('#usermailVal').val()
            var passwordval = $('#passwordVal').val()
            $.ajax({
                url: 'login',
                type: 'POST',
                dataType: 'json',
                data: {
                    usermail: usermailval,
                    password: passwordval
                }
            }).done(function(data){
                if (data['status'] == 'successful') {
                    alert(data['message'])
                    location.reload();
                }else{
                    alert(data['message'])
                }
            })
            e.preventDefault();
        })

        $('#registForm').on('submit', function(e){
            var usermailval = $('#registUsermailVal').val()
            var nicknameval = $('#registNicknameVal').val()
            var passwordval1 = $('#passwordVal1').val()
            var passwordval2 = $('#passwordVal2').val()
            $.ajax({
                url: 'register',
                type: 'POST',
                dataType: 'json',
                data: {
                    usermail: usermailval,
                    nickname: nicknameval,
                    password1: passwordval1,
                    password2: passwordval2
                }
            }).done(function(data){
                if (data['status'] == 'successful') {
                    alert(data['message']) 
                }else{
                    alert(data['message'])
                }
            })
            e.preventDefault();
        })
    }
})

