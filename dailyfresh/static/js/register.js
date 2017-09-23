$(function(){

	var error_name = false;
	var error_password = false;
	var error_check_password = false;
	var error_email = false;
	var error_check = false;


	$('#user_name').blur(function() {
		// 校验用户名长度是否合法
		check_user_name();
		if (error_name == false){
			// 校验用户名是否存在
			// check_user_name_exist()
			check_user_name_exist(true)
		}
	}).click(function () {
		$('#user_name').next().hide();
    });

	$('#pwd').blur(function() {
		check_pwd();
	}).click(function () {
		$('#pwd').next().hide()
    });

	$('#cpwd').blur(function() {
		check_cpwd();
	}).click(function () {
		$('#cpwd').next().hide()
    });

	$('#email').blur(function() {
		check_email();
	}).click(function () {
		$('#email').next().hide()
    });

	$('#allow').click(function() {
		if($(this).is(':checked'))
		{
			error_check = false;
			$(this).siblings('span').hide();
		}
		else
		{
			error_check = true;
			$(this).siblings('span').html('请勾选同意');
			$(this).siblings('span').show();
		}
	});


	function check_user_name(){
		var len = $('#user_name').val().length;
		if(len<5||len>20)
		{
			$('#user_name').next().html('请输入5-20个字符的用户名')
			$('#user_name').next().show();
			error_name = true;
		}
		else
		{
			$('#user_name').next().hide();
			error_name = false;
		}
	}

	// 校验用户名是否存在
	// function check_user_name_exitst() {
	// 	// 1.获取用户名
	// 	username =  $('#user_name').val()
	// 	// 2.发起一个ajax请求,把username作为参数传过去
	// 	$.get('/uesr/check_user_exist/?username='+username, function (data) {
	// 		// 如果用户名存在　返回{'res':0} 用户不存在,返回{'res':1}
	// 		if(data.res == 0){
	// 			$('#user_name').next().show().text('用户名已注册');
	// 			error_name = true;
	// 		}
	// 		else
	// 		{
	// 			$('#user_name').next().hide();
	// 			error_name = false;
	// 		}
     //    })
    // }
    // function check_user_name_exitst() {
		// username = $('#user_name').val()
		// $.post('/user/check_user_exist/',{'username':username},function (data) {
		// 	if(data.res == 0){
		// 		$('#user_name').next().show().text('用户名已注册');
		// 		error_name = true;
		// 	}
		// 	else
		// 	{
		// 		$('#user_name').next().hide();
		// 		error_name = false;
		// 	}
    //     })
    // }

	// ajax默认异步执行　async:true 为异步执行　async:false 为同步执行
	function check_user_name_exist(async) {
		// 1.获取用户名
		username = $('#user_name').val()
		// alert(username)
		// 2.发起ajax请求
		$.ajax({
			url:'/user/check_user_exist/',
			async:async,
			data: {'username':username},
		})
			.done(function (data) {
				// alert(2)
				// 如果用户名存在,返回{'res':0} 用户名不存在,返回{'res':1}
				if(data.res == 0){
					$('#user_name').next().text('用户名已注册').show();
					error_name = true;
				}
				else
				{
					// alert(3)
					$('#user_name').next().hide();
					error_name = false;
				}
            })

    }

	function check_pwd(){
		var len = $('#pwd').val().length;
		if(len<8||len>20)
		{
			$('#pwd').next().html('密码最少8位，最长20位');
			$('#pwd').next().show();
			error_password = true;
		}
		else
		{
			$('#pwd').next().hide();
			error_password = false;
		}		
	}


	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass)
		{
			$('#cpwd').next().html('两次输入的密码不一致')
			$('#cpwd').next().show();
			error_check_password = true;
		}
		else
		{
			$('#cpwd').next().hide();
			error_check_password = false;
		}		
		
	}

	function check_email(){
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

		if(re.test($('#email').val()))
		{
			$('#email').next().hide();
			error_email = false;
		}
		else
		{
			$('#email').next().html('你输入的邮箱格式不正确')
			$('#email').next().show();
			error_check_password = true;
		}

	}


	$('#reg_form2').submit(function() {
		check_user_name();
		check_pwd();
		// 再次校验
		check_user_name_exist(false) // 同步阻塞执行查询过程
		check_cpwd();
		check_email();

		if(error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});








})