/**
 * __author__ = 'Stacy E. Webb'
 *__date__ = '2/26/2011'
 */

package com.coursesmart.servicehub.servlet.service;

import java.util.Map;

public interface IOAuthService {
	/**
	 * Perform a service given in incoming <paramMap>.
	 * Service returns an outgoing map of results.
	 * 
	 * @param paramMap paramMap of app-specific name/value pairs
	 * @return result set in a Map
	 */
	public Map<String,String> doService(Map<String, String> paramMap);
}
