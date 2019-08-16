docker rmi $(docker image ls | grep "\(docker-airflow\|<none>\)" | sed 's/ \{1,\}/,/g' | cut -d, -f3)
