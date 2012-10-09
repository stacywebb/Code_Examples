/**
 * __author__ = 'Stacy E. Webb'
 *__date__ = '2/26/2011'
 */

package com.coursesmart.servicehub.servlet.service;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Lookup firstname, lastname, email, and roles for given 'userId'.
 * If service errors put 'oauth_error_code' and 'oauth_error_message' into resultMap.
 *
 */
public class GetUserInfoService implements IOAuthService {

	public Map<String, String> doService(Map<String, String> paramMap) {
		Map<String,String> resultMap = new LinkedHashMap<String, String>();
		String userId = paramMap.get("userId");
		/*
		 * Put your own user information algorithm here...
		 */
		// the following code is for test purposes only
		if (userId == null) {
			resultMap.put("oauth_error_code", "NoSuchUser");
			resultMap.put("oauth_error_message", "There is no user");
		} else {

			resultMap.put("firstname", "first_"+userId);
			resultMap.put("lastname", "last_"+userId);
			resultMap.put("email", userId+"@example.com");	
			resultMap.put("roles", "Instructor,SysAdmin");
		}
		/*
		 * End of user information algorithm section...
		 */
		
		return resultMap;
	}

}
