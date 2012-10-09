/**
 * __author__ = 'Stacy E. Webb'
 *__date__ = '2/26/2011'
 */


package com.coursesmart.servicehub.servlet;

import java.io.IOException;
import java.util.Map;
import java.util.LinkedHashMap;

import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.coursesmart.servicehub.security.OAuthUtil;
import com.coursesmart.servicehub.servlet.service.IOAuthService;
import com.google.gson.Gson;


public class OAuthLiteServlet extends HttpServlet
{
	private static final long serialVersionUID = -4644908152796052849L;

	private static final String TEST_USER = "__testuser__";

	/**
	 * This three parameters personalize your token validation.
	 * The exact values for these should be procured from CourseSmart.
	 * TENANT_NAME and KEY_NAME are public to anyone and are included in cleartext in the token.
	 * SHARED_SECRET should be kept private except from CourseSmart.
	 */

	private String key_name = null;
	private String sharedSecret = null;
	
	public void init(ServletConfig config) throws ServletException {
		super.init(config);
		this.key_name = config.getInitParameter("key");
		this.sharedSecret = config.getInitParameter("secret");
	}

	private String createErrorResponse(String errorCode, String errorMessage)
	{
		Map<String,String> resultMap = new LinkedHashMap<String,String>();
		resultMap.put("outh_error_code", errorCode);
		resultMap.put("outh_error_message", errorMessage);
		String result = createResponse(resultMap);
		return result;
	}
	
	private String createResponse(Map<String,String> resultMap)
	{
		Gson gson = new Gson();
		String result = gson.toJson(resultMap);
		return result;
	}
	
	/**
	 * Call {@link #processRequest}.
	 */
	public final void doGet(HttpServletRequest request,
			HttpServletResponse response) throws IOException
	{
		String result = null;
		Map<String, String> requestMap = null;
		try {
			requestMap = OAuthUtil.verifySignedRequest(request, key_name, sharedSecret);
		} catch (Exception e1) {
			response.getWriter().write(createErrorResponse("OAuthVerificationError", 
					"Error attempting to verify the request"));
			return;
		}

		String requestURI = request.getRequestURI().trim();
		if (requestURI == null || requestURI.length() == 0) {
			response.getWriter().write(createErrorResponse("NoServiceSpecified", 
				"Service name must be at end of the URL"));
			return;
		}
		String[] tokens = requestURI.split("/");
		String serviceName = tokens[tokens.length-1];
		
		Class<IOAuthService> clazz;
		IOAuthService service = null;
		String className = null;
		try {
			className = "com.coursesmart.servicehub.servlet.service." + serviceName;
			clazz = (Class<IOAuthService>)Class.forName(className);
			service = clazz.newInstance();
		} catch (Exception e) {
			response.getWriter().write(createErrorResponse("CantCreateService", 
				"Service class " + className + " can't be instantiated"));
			return;
		}
		
		Map<String,String> resultMap = service.doService(requestMap);
		result = createResponse(resultMap);
		response.getWriter().write(result);
	}
	
	/**
	 * Call {@link #processRequest}.
	 */
	public final void doPost(HttpServletRequest request,
			HttpServletResponse response)
	{
		try {
			doGet(request, response);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
