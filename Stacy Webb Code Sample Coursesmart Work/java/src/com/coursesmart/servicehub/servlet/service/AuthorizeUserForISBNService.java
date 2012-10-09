/**
 * __author__ = 'Stacy E. Webb'
 *__date__ = '2/26/2011'
 */

package com.coursesmart.servicehub.servlet.service;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Authorize a given 'userId' for a given 'ISBN'.
 * If service errors put 'oauth_error_code' and 'oauth_error_message' into resultMap.
 *
 */
public class AuthorizeUserForISBNService implements IOAuthService {

	public Map<String, String> doService(Map<String, String> paramMap) {
		Map<String,String> resultMap = new LinkedHashMap<String, String>();
		/**
		 * Put in your authorization logic here.
		 */
		resultMap.put("authorize", "true");
		
		return resultMap;
	}

}
