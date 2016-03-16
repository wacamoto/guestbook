if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined'
        ? args[number]
        : ''
      ;
    });
  };
}

itemList = function() {
    this.data;
    this.itemBox = $('#commentItem')
    var html = '<div class="item">\
                    <div class="middle aligned content">\
                        <a class="header" href="{0}">{1}</a>\
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
                'url': 'getboard',
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
            $.post('newboard', {
                page_url: url
            }).done(function(data){
                alert(data)
            })
            e.preventDefault();

            // refresh page
            boardList.update()
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
            var passwordval1 = $('#passwordVal1').val()
            var passwordval2 = $('#passwordVal2').val()
            $.post('register', {
                usermail: usermailval,
                password1: passwordval1,
                password2: passwordval2
            }).done(function(data){
                alert(data)
            })
            e.preventDefault();
        })
    }
})

