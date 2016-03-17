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
            $.post('board', {
                board_url: url
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
                success: function(data) {
                    alert(data)
                    boardList.update()
                }
            })
            console.log('board?board_id=' + $(this).attr('id'))
        })
        
    } else {
        $('#loginForm').submit(function(){
            var usermailval = $('#usermailVal').val()
            var passwordval = $('#passwordVal').val()
            $.post('login', {
                usermail: usermailval,
                password: passwordval
            }).done(function(data){
                alert(data)
            })
            e.preventDefault();
        })

        $('#registForm').on('submit', function(){
            var usermailval = $('#registUsermailVal').val()
            var nicknameval = $('#registNicknameVal').val()
            var passwordval1 = $('#passwordVal1').val()
            var passwordval2 = $('#passwordVal2').val()
            $.post('register', {
                usermail: usermailval,
                nickname: nicknameval,
                password1: passwordval1,
                password2: passwordval2
            }).done(function(data){
                alert(data)
            })
            e.preventDefault();
        })
    }
})

