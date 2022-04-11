// ユーザープールの設定
const poolData = {
    UserPoolId : 'XXX',
    ClientId : 'XXX'
};
const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
const cognitoUser = userPool.getCurrentUser();  // 現在のユーザー
 
var currentUserData = {};  // ユーザーの属性情報
 
/**
 * 画面読み込み時の処理
 */
$(document).ready(function() {
 
    // Amazon Cognito 認証情報プロバイダーの初期化
    AWS.config.region = 'XXX'; // リージョン
    AWS.config.credentials = new AWS.CognitoIdentityCredentials({
        IdentityPoolId: 'XXX'
    });
		    
    // 現在のユーザーの属性情報を取得・表示
    getUserAttribute();
});
 
/**
 * 現在のユーザーの属性情報を取得・表示する
 */
var getUserAttribute = function(){
	
    // 現在のユーザー情報が取得できているか？
    if (cognitoUser != null) {
        cognitoUser.getSession(function(err, session) {
            if (err) {
                console.log(err);
                $(location).attr("href", "signin.html");
            } else {
                // ユーザの属性を取得
                cognitoUser.getUserAttributes(function(err, result) {
                    if (err) {
                        $(location).attr("href", "signin.html");
                    }
                    //console.log(cognitoUser.signInUserSession.idToken.jwtToken);
                    //alert("ログイン済みです");
                });
            }
        });
    } else {
        $(location).attr("href", "signin.html");
    }
};