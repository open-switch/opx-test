#!/usr/bin/groovy

import jenkins.security.*
//j.jenkins.setSecurityRealm(j.createDummySecurityRealm());
User u = User.get("admin")
ApiTokenProperty t = u.getProperty(ApiTokenProperty.class)
def token = t.getApiTokenInsecure()

//User u = User.get("admin")
//ApiTokenProperty t = u.getProperty(ApiTokenProperty.class)
//def token = t.getApiTokenInsecure()
//token.getClass()
println "token is $token "
