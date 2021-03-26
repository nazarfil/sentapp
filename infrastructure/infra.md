## Infrastructure overview

### AWS
    Elastic Beanstalk                   : EC2 VM running images of app + redis
    RDS PostgresSql (t2.micro) instance : DB on EB network
    Cloudfront                          : Nameserver
    Elastic Loadbalancer                : HTTPS
    ECR                                 : Docker iamge of the app

### Not AWS
    Go Daddy                            : DNS registry
    Vercel                              : Static frontend   
