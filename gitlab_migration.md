## Migracja Gitlab
<br>
Zestaw komend API call pozwalający na migrację wielu repozytoriów z jednej instancji ( git1.example.pl ) Gitalb na drugą ( git2.example.pl ) .
Przetestowany w boju :-)
<br>
Zmienne:

```
gl_skad_url="https://git1.example.pl/api/v4";
gl_skad_token="xxxxxxxxxxxx";
gl_dokad_url="https://git2.example.pl/api/v4";
gl_dokad_token="yyyyyyyyyyyyyyy";
```
<br>

### List projects variables on git1

```
grupa_id=87; for repo_id in $(curl -s "$gl_skad_url/groups/$grupa_id?private_token=$gl_skad_token" | jq '.projects[].id' | tr -d '"'); do  curl --request GET --header "PRIVATE-TOKEN: $gl_skad_token" "$gl_skad_url/projects/$repo_id/variables" | jq '.'; done;
```

### List project archive status
```
 grupa_id=77; for repo_id in $(curl -s --request GET "$gl_dokad_url/groups/$grupa_id?private_token=$gl_dokad_token" | jq '.projects[].id' | tr -d '"' ); do curl -s --request GET --header "PRIVATE-TOKEN: $gl_dokad_token" "$gl_dokad_url/projects/$repo_id" | jq '.name, .archived' ; done; echo;
```

## Schedule gitlab export on git1
```
grupa_id=10; for repo_id in $(curl -s "$gl_skad_url/groups/$grupa_id?private_token=$gl_skad_token" | jq '.projects[].id' | tr -d '"'); do  curl --request POST --header "PRIVATE-TOKEN: $gl_skad_token" "$gl_skad_url/projects/$repo_id/export"; done;
```

### Check export status on git1
```
grupa_id=10; for repo_id in $(curl -s "$gl_skad_url/groups/$grupa_id?private_token=$gl_skad_token " | jq '.projects[].id' | tr -d '"'); do curl -s --request GET --header "PRIVATE-TOKEN: $gl_skad_token" "$gl_skad_url/projects/$repo_id/export" | jq '.export_status' ; done;
```

### Download export from git1
```
grupa_id=10;for repo_id in $(curl "$gl_skad_url/groups/$grupa_id?private_token=$gl_skad_token" | jq '.projects[].id' | tr -d '"'); do curl --header "PRIVATE-TOKEN: $gl_skad_token" --remote-header-name --remote-name "$gl_skad_url/projects/$repo_id/export/download" && repo_name=$(curl "$gl_skad_url/projects/$repo_id?private_token=$gl_skad_token" | jq '.name' | tr -d '"');stara_nazwa=$(ls -tr | grep -v total | tail -n 1); mv $stara_nazwa  "$repo_name-$stara_nazwa"; done; ls -lha;
```

### Schedule import to git2
```
 grupa_name=ros; IFS=$(echo -en "\n\b"); for repo_export in $(ls *2020-09* ); do echo -e "\n----------------"; echo $( echo $repo_export  | awk -F '-2020' '{ print $1 }'); curl --request POST --header "PRIVATE-TOKEN: $gl_dokad_token" --form "name=$(ls $repo_export | awk -F '-2020' '{ print $1 }')" --form "namespace=$grupa_name" --form "path=$(ls $repo_export | awk -F '-2020' '{ print $1 }' | tr '[:upper:]' '[:lower:]' | tr ' ' '-')" --form "file=@$repo_export" "$gl_dokad_url/projects/import"; done; echo;
```

### Check import status
```
grupa_name=ros; grupa_id=77; for repo_id in $(curl -s --request GET "$gl_dokad_url/groups/$grupa_id?private_token=$gl_dokad_token" | jq '.projects[].id' | tr -d '"' ); do curl -s --request GET --header "PRIVATE-TOKEN: $gl_dokad_token" "$gl_dokad_url/projects/$repo_id/import" | jq '.name, .import_status';echo; done; echo;
```


### (Un)Archive projects
```
 grupa_id=77; for repo_id in $(curl -s --request GET "$gl_dokad_url/groups/$grupa_id?private_token=$gl_dokad_token" | jq '.projects[].id' | tr -d '"' ); do curl -s --request POST --header "PRIVATE-TOKEN: $gl_dokad_token" "$gl_dokad_url/projects/$repo_id/unarchive" | jq '.archived' ; done; echo;
```

### (optional)
### List GL local users

```
for czlonek in $( curl -s --request GET --header "PRIVATE-TOKEN: $gl_dokad_token" "$gl_dokad_url/users?per_page=50" | jq '.[].id' ); do if [ -z $( curl -s --request GET --header "PRIVATE-TOKEN: $gl_dokad_token" "$gl_dokad_url/users/$czlonek/" | jq '.identities[].provider' ) ]; then curl -s --request GET --header "PRIVATE-TOKEN: $gl_dokad_token" "$gl_dokad_url/users/$czlonek/" | jq '.username'; echo "lokalny"; fi; done; echo;
```

### Search for projects containing WIKI

```
gl_skad_token=xxxxxxxxxxxxxxxx
gl_skad_url=https://git1.example.pl/api/v4
```
```
grupa_id=182;for repo_id in $(curl -s --header "PRIVATE-TOKEN: " "$gl_skad_token/groups/$grupa_id" | jq '.projects[].id' | tr -d '"'); do  repo_name=$(curl -s --request GET --header "PRIVATE-TOKEN: $gl_skad_token" "$gl_skad_url/projects/$repo_id" | jq '.name' | tr -d '"'); wiki_tytul=""; wiki_tytul=$(curl -s --request GET --header "PRIVATE-TOKEN: $gl_skad_token" "$gl_skad_url/projects/$repo_id/wikis" | jq '.[].title' | tr -d '"'); [ ! -z "$wiki_tytul" ] && echo -e "$repo_id $repo_name \n$wiki_tytul \n ------------------------------\n"; done;
```
