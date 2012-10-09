/**
 * __author__ = 'Stacy E. Webb'
 *__date__ = '2/26/2011'
 */

package com.coursesmart.servicehub.servlet.service;

import java.util.Map;

public class EchoOAuthService implements IOAuthService {

	/**
	 * Echos incoming paramMap back to result map.
	 */
	public Map<String, String> doService(Map<String, String> paramMap) {
		return paramMap;
	}

}
