const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => container.classList.add('right-panel-active'));
signInButton.addEventListener('click', () => container.classList.remove('right-panel-active'));

function signUpFuntion() {

	let userId = document.getElementById("userIdSignUp"); //用户名

	let password = document.getElementById("passwordSignUp"); //密码
	let confirmPassword = document.getElementById("confirmPasswordSignUp"); //确认密码

	let email = document.getElementById("emailSignUp"); //邮箱

	if (userId.value.length == 0 || email.value.length == 0 || password.value.length == 0) {
		alert("用户名、账号或密码为空！");
		return false;
	} else if (password.value != confirmPassword.value) {
		alert("密码不一致");
		return false;
		// window.location.href = "#";
	} else {
		alert("注册成功!开始使用吧");
		document.getElementById("sign-up-container").submit();
	}

}

function signInFuntion() {
	let account = document.getElementById("accountSignIn"); //账号
	let password = document.getElementById("passwordSignIn"); //密码


	if (account.value.length == 0 || password.value.length == 0) {
		alert("账号或密码为空！");
		return false;
		// window.location.href = "#";
		
	} else {
		alert("登录成功!");
		// window.location.href = "index.html";
		// document.getElementById("sign-in-container").submit();
		return true;
	}

}

function socialFuntion() {
	alert("这些还不可用！");
	
}

function forgetFuntion() {
	alert("随便输入就行啦！");
	
}


function success() {
	alert("成功登入！");

}