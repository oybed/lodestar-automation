import json
import datetime

subject = context["repositories"]

status = {
  "overall_status": "",
  "messages": [],
  "subsystems": []
}
ocp_subsystem = {
  "name": "openshift",
  "status": "",
  "state": "",
  "info": "",
  "updated": "",
  "access_urls": [],
  "messages": []
}

with open(f"../../{subject['directory']}/engagement.json", "r") as read_file:
  engagement = json.load(read_file)

current_state = subject["anarchy_subject"]["spec"]["vars"]["current_state"]
desired_state = subject["anarchy_subject"]["spec"]["vars"]["desired_state"]

ocp_subsystem["status"] = "green" if current_state == desired_state else "yellow"
ocp_subsystem["state"] = current_state
ocp_subsystem["info"] = "Working as expected" if current_state == desired_state else "Contact SRE team"
ocp_subsystem["updated"] = str(datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc, microsecond=0).isoformat())
ocp_subsystem["access_urls"] = [
  {
    "Web Console": f"https://console-openshift-console.apps.{engagement['ocp_sub_domain']}.{context["ocp_base_url"]}"
  },
  {
    "API": f"https://api.{engagement['ocp_sub_domain']}.{context["ocp_base_url"]}:6443"
  }
]

status["overall_status"] = ocp_subsystem["status"]
status["subsystems"].append(ocp_subsystem)

with open(f"../../{subject['directory']}/status.json", 'w') as fp:
  json.dump(status, fp)
