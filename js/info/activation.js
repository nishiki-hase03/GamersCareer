// ユーザープールの設定
const poolData = {
    UserPoolId : 'XXX',
    ClientId : 'XXX'
};
const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
 
/**
 * 画面読み込み時の処理
 */
$(document).ready(function() {
	
	// Amazon Cognito 認証情報プロバイダーの初期化
	AWS.config.region = 'XXX'; // リージョン
	AWS.config.credentials = new AWS.CognitoIdentityCredentials({
	    IdentityPoolId: 'XXX'
	});
	
	// 「Activate」ボタン押下時
	$("#activationButton").click(function(event) {
	    activate();
	});
});
 
/**
 * アクティベーション処理
 */
var activate = function() {
 
    var email = $("#email").val();
    var activationKey = $("#activationKey").val();
    
    // 何か1つでも未入力の項目がある場合、処理を中断
    if (!email | !activationKey) {
        return false;
    } 
	
    var userData = {
        Username : email,
        Pool : userPool
    };
    var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
    
    // アクティベーション処理
    cognitoUser.confirmRegistration(activationKey, true, function(err, result){
        if (err) {
            // アクティベーション失敗の場合、エラーメッセージを画面に表示
            if (err.message != null) {
                $("div#message span").empty();
                $("div#message span").append(err.message);
            }
        } else {
            // アクティベーション成功の場合、サインイン画面に遷移
            alert("アカウントの有効化に成功しました");
            
            // ユーザ情報を登録
            var apiurl = "https://XXX/putUserProfile";
            var data = {
                'email': email
            }
            $.ajax({
                url: apiurl,
                type: 'POST',
                dataType: 'json',
                data: JSON.stringify(data)
            })
            .done(function(response) {
                alert('成功です');
                window.location.href = './signin.html';
            })
            .fail(function(jqXHR, textStatus, errorThrown) {
                alert('エラーです');
            })
            
        }
    });
};