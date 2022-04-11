// 1Amazon Cognito 認証情報プロバイダーを初期化します
// Amazon Cognito 認証情報プロバイダーを初期化します
AWS.config.region = 'XXX'; // リージョン
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
  IdentityPoolId: 'XXX',
});
//よくわからないけど初期化します
AWSCognito.config.region = 'XXX'; // リージョン(デフォルトだとこのまま)
AWSCognito.config.credentials = new AWS.CognitoIdentityCredentials({
  IdentityPoolId: 'XXX', // ID プールのID
});