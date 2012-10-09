/**
 * __author__ = 'Stacy E. Webb'
 *__date__ = '2/26/2011'
 */

package com.coursesmart.servicehub.servlet;

import java.util.Map;
import java.util.TreeMap;

import net.oauth.client.OAuthClient;

import org.apache.commons.httpclient.HttpClient;

import com.coursesmart.servicehub.security.OAuthUtil;

public class TestOAuthServlet {

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception{
		// On 0 args or incomplete name-value combination
		if (args.length < 5 | (args.length % 2) == 0) {
			System.out.println("usage:  TestOAuthServlet <url> (<name> <value>)*");
			System.out.println("        <url>   		::= name of the Java class for this service");
			System.out.println("        <key>   		::= key identifier");
			System.out.println("        <sharedSecret>	::= shared secret");
			System.out.println("        <args>  		::= any number of name/value pairs to pass to OAuthService");
			System.out.println("e.g. java TestOAuthServlet EchoOAuthService name jack zip 22112");
			System.out.println("     will execute the EchoOAuthService and then display result map");
			System.exit(1);
		}

		// get arguments
		String url = args[0];
		String key = args[1];
		String sharedSecret = args[2];
		
		int numberOfPairs = (args.length-3) / 2;
		Map<String,String> inMap = new TreeMap<String, String>();
		for (int i = 0; i < numberOfPairs; i++) {
			String name = args[(i*2)+1];
			String value = args[(i*2)+2];
			inMap.put(name, value);
		}
		
		Map<String,String> resultMap = OAuthUtil.postSignedRequest(url, inMap, key, sharedSecret);
		
		for (Map.Entry<String, String> entry : resultMap.entrySet()) {
			System.out.println(entry.getKey() + ": " + entry.getValue());
		}
	}

}
