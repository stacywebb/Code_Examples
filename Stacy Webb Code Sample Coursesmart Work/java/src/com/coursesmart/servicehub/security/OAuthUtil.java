/**
 * __author__ = 'Stacy E. Webb'
 *__date__ = '2/26/2011'
 */

package com.coursesmart.servicehub.security;

import java.lang.reflect.Type;
import java.util.Collection;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Map.Entry;

import javax.servlet.http.HttpServletRequest;

import net.oauth.OAuth;
import net.oauth.OAuthAccessor;
import net.oauth.OAuthConsumer;
import net.oauth.OAuthMessage;
import net.oauth.OAuthValidator;
import net.oauth.SimpleOAuthValidator;
import net.oauth.client.OAuthClient;
import net.oauth.client.OAuthResponseMessage;
import net.oauth.client.httpclient4.HttpClient4;
import net.oauth.server.OAuthServlet;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

public class OAuthUtil {
	
	public static Type typeOfMap = new TypeToken<Map<String, String>>() {}.getType();


	public static void main(String[] args) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("firstname", "<Insert_Local_User_First_Name>");
		params.put("lastname", "<Insert_Local_User_Last_Name>");
		String url = "http://localhost:8000/ServiceHub/lti/ltiservice/";
		System.out.println(postSignedRequest(url, params, "12345", "secret"));
	}

	public static Map<String,String> postSignedRequest(String url,
			Map<String, String> params, String key, String sharedSecret)
			throws Exception {
		Map<String,String> result = null;

		OAuthMessage message = new OAuthMessage("POST", url,
				(Collection<? extends Entry>) params.entrySet());
		OAuthConsumer consumer = new OAuthConsumer(null, key, sharedSecret,
				null);
		consumer.setProperty(OAuth.OAUTH_SIGNATURE_METHOD, OAuth.HMAC_SHA1);

		OAuthAccessor accessor = new OAuthAccessor(consumer);
		message.addRequiredParameters(accessor);
		OAuthClient client = new OAuthClient(new HttpClient4());
		OAuthResponseMessage responseMessage = (OAuthResponseMessage) client
				.invoke(accessor, "POST", url, params.entrySet());
		String resultString = responseMessage.readBodyAsString();

		Gson gson = new Gson();
		
		result = gson.fromJson(resultString, typeOfMap);
		
		return result;
	}

	public static Map<String, String> verifySignedRequest(
			HttpServletRequest request, String key, String sharedSecret)
			throws Exception {
		Map<String, String> result = new HashMap<String, String>();
		OAuthMessage message = OAuthServlet.getMessage(request, null);
		OAuthValidator validator = new SimpleOAuthValidator();
		if (request.getParameter("oauth_consumer_key") == null) {
			throw new IllegalArgumentException(
					"OAuth error: Missing oauth_consumer_key");
		}

		OAuthConsumer consumer = new OAuthConsumer(null, key, sharedSecret,
				null);
		OAuthAccessor accessor = new OAuthAccessor(consumer);

		validator.validateMessage(message, accessor);

		Map<String, String[]> parameterMap = request.getParameterMap();
		for (Map.Entry<String, String[]> param : parameterMap.entrySet()) {
			if (!param.getKey().startsWith("oauth_")) {
				result.put(param.getKey(), param.getValue()[0]);
			}
		}

		return result;
	}
}
