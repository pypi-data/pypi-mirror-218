
{% macro cratedb__create_table_as(temporary, relation, sql) -%}
  {%- call statement('check_relation_exists', fetch_result=True) -%}
    select count(*) from "information_schema"."tables" where table_name='{{ relation.identifier }}' and table_schema='{{ relation.schema }}';
  {% endcall %}

  {% set relation_exists = load_result('check_relation_exists') %}

  {% if relation_exists['data'][0][0] == 0 %}
    create table {{ relation }}
      as (
        {{ sql }}
      );
  {% endif %}

{%- endmacro %}

{% macro cratedb__get_columns_in_relation(relation) -%}
  {% call statement('get_columns_in_relation', fetch_result=True) %}
      select
          column_name,
          data_type,
          character_maximum_length,
          numeric_precision,
          numeric_scale

      from {{ relation.information_schema('columns') }}
      where table_name = '{{ relation.identifier }}'
        {% if relation.schema %}
        and table_schema = '{{ relation.schema }}'
        {% endif %}
      order by ordinal_position

  {% endcall %}
  {% set table = load_result('get_columns_in_relation').table %}
  {{ return(sql_convert_columns_in_relation(table)) }}
{% endmacro %}

{% macro cratedb__list_relations_without_caching(schema_relation) %}
  {% call statement('list_relations_without_caching', fetch_result=True) -%}
    select
      '{{ schema_relation.database }}' as database,
      table_name as name,
      table_schema as schema,
      'table' as type
    from information_schema.tables
    where table_schema ilike '{{ schema_relation.schema }}'
    union all
    select
      '{{ schema_relation.database }}' as database,
      table_name as name,
      table_schema as schema,
      'view' as type
    from information_schema.views
    where table_schema ilike '{{ schema_relation.schema }}'
  {% endcall %}
  {{ return(load_result('list_relations_without_caching').table) }}
{% endmacro %}

{% macro cratedb__current_timestamp() -%}
  now()
{%- endmacro %}


{% macro cratedb__create_view_as(relation, sql) -%}
  create view {{ relation }} as
    {{ sql }};
{% endmacro %}


{% macro cratedb__rename_relation(from_relation, to_relation) -%}
  {% call statement('rename_relation') -%}
    alter table {{ from_relation }} rename to {{ to_relation.name }}
  {%- endcall %}
{% endmacro %}

{% macro cratedb__create_schema(relation) -%}
  {%- call statement('create_schema') -%}
    commit;
  {%- endcall -%}
{% endmacro %}

{% macro cratedb__list_schemas(database) -%}
    {% call statement('list_schemas', fetch_result=True, auto_begin=False) %}
      show schemas;
    {% endcall %}
    {{ return(load_result('list_schemas').table) }}
{% endmacro %}

{% macro cratedb__drop_relation(relation) -%}
  {% call statement('drop_relation', auto_begin=False) -%}
    drop {{ relation.type }} if exists {{ relation }}
  {%- endcall %}
{% endmacro %}

{% macro rename_view_relation(from_relation, to_relation) -%}
  {{ return(adapter.dispatch('rename_view_relation', 'dbt')(from_relation, to_relation)) }}
{% endmacro %}

{% macro cratedb__rename_view_relation(from_relation, to_relation) -%}
    {% call statement('get_view_definition', fetch_result=True, auto_begin=False) %}
        SELECT view_definition
        FROM information_schema.views
        WHERE table_schema = '{{from_relation.schema}}'
        AND table_name = '{{from_relation.name}}' limit 1;
    {%- endcall %}
    {% set result = load_result('get_view_definition') -%}

    {% if result['data'] != [] %}
        {% set view_definition = result["data"][0][0] -%}

        {% call statement('drop_view') -%}
            drop view if exists {{ from_relation }};
        {% endcall %}

        {% call statement('create_view', fetch_result=True, auto_begin=False) -%}
            {{adapter.dispatch('create_view_as', 'dbt')(to_relation, view_definition)}}
        {% endcall %}
        {% set create_view_result = load_result('create_view') -%}
        {{return(result)}}
    {% endif %}

    {{return("")}}
{% endmacro %}