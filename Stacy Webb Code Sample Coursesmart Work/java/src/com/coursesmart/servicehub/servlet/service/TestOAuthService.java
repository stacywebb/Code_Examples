/**
 * __author__ = 'Stacy E. Webb'
 *__date__ = '2/26/2011'
 */

package com.coursesmart.servicehub.servlet.service;

import java.util.Map;
import java.util.TreeMap;

public class TestOAuthService {

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception{
		// On 0 args or incomplete name-value combination
		if (args.length < 3 | (args.length % 2) == 0) {
			System.out.println("usage:  TestOAuthService <service-class-name> (<name> <value>)*");
			System.out.println("        <service-class-name> ::= name of the Java class for this service");
			System.out.println("        <args>               ::= any number of name/value pairs to pass to OAuthService");
			System.out.println("e.g. java TestOAuthService EchoOAuthService name jack zip 22112");
			System.out.println("     will execute the EchoOAuthService and then display result map");
			System.exit(1);
		}

		// get arguments
		String serviceClassName = args[0];
		int numberOfPairs = (args.length-1) / 2;
		Map<String,String> inMap = new TreeMap<String, String>();
		for (int i = 0; i < numberOfPairs; i++) {
			String name = args[(i*2)+1];
			String value = args[(i*2)+2];
			inMap.put(name, value);
		}
		
		Class<IOAuthService> clazz 
			= (Class<IOAuthService>)Class.forName("com.coursesmart.servicehub.servlet.service." + serviceClassName);
		IOAuthService service = clazz.newInstance();
		
		Map<String,String> resultMap = service.doService(inMap);
		if (resultMap == null) {
			System.out.println("Result is vacuous");
		} else {
			for (Map.Entry<String, String> entry : resultMap.entrySet()) {
				System.out.println(entry.getKey() + ": " + entry.getValue());
			}
		}
	}

}
