from homeassistant.components.number import ATTR_VALUE, DOMAIN as NUMBER_DOMAIN
from homeassistant.components.number.const import SERVICE_SET_VALUE
from homeassistant.const import ATTR_ENTITY_ID, ATTR_FRIENDLY_NAME
from homeassistant.helpers.entity_component import async_update_entity

from custom_components.smartbox.const import DOMAIN

from .mocks import (
    get_boost_duration_entity_id,
    get_boost_duration_entity_name,
    get_boost_temperature_entity_id,
    get_boost_temperature_entity_name,
    get_entity_id_from_unique_id,
    get_node_unique_id,
    get_object_id,
    get_power_limit_number_entity_id,
    get_power_limit_number_entity_name,
)


async def test_power_limit(hass, mock_smartbox, config_entry):
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert len(hass.states.async_entity_ids(NUMBER_DOMAIN)) == 11
    entries = hass.config_entries.async_entries(DOMAIN)
    assert len(entries) == 1

    assert DOMAIN in hass.config.components
    for mock_device in await mock_smartbox.session.get_devices():
        mock_node = (await mock_smartbox.session.get_nodes(mock_device["dev_id"]))[0]
        if mock_node["type"] == "pmo":
            entity_id = get_power_limit_number_entity_id(mock_node)
            state = hass.states.get(entity_id)
            # check basic properties
            assert state.object_id.startswith(
                get_object_id(get_power_limit_number_entity_name(mock_node))
            )
            assert state.entity_id.startswith(
                get_power_limit_number_entity_id(mock_node)
            )
            assert state.name == f"{mock_node['name']} Power Limit"
            assert (
                state.attributes[ATTR_FRIENDLY_NAME]
                == f"{mock_node['name']} Power Limit"
            )
            unique_id = get_node_unique_id(mock_device, mock_node, "power_limit")
            assert entity_id == get_entity_id_from_unique_id(
                hass, NUMBER_DOMAIN, unique_id
            )

            # Starts not away
            assert state.state == "1000"

    mock_device_2 = (await mock_smartbox.session.get_devices())[1]
    mock_node_2 = (await mock_smartbox.session.get_nodes(mock_device_2["dev_id"]))[0]
    entity_id = get_power_limit_number_entity_id(mock_node_2)
    await async_update_entity(hass, entity_id)
    state = hass.states.get(entity_id)
    assert state.state == "1000"

    entity_id = get_power_limit_number_entity_id(mock_node_2)
    await hass.services.async_call(
        NUMBER_DOMAIN,
        SERVICE_SET_VALUE,
        {ATTR_ENTITY_ID: entity_id, ATTR_VALUE: 500},
        blocking=True,
    )
    await async_update_entity(hass, entity_id)
    state = hass.states.get(entity_id)
    assert state.state == "500"


async def test_boost_temperature(hass, mock_smartbox, config_entry):
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert len(hass.states.async_entity_ids(NUMBER_DOMAIN)) == 11
    entries = hass.config_entries.async_entries(DOMAIN)
    assert len(entries) == 1

    assert DOMAIN in hass.config.components
    mock_device = (await mock_smartbox.session.get_devices())[1]
    mock_node = (await mock_smartbox.session.get_nodes(mock_device["dev_id"]))[3]
    entity_id = get_boost_temperature_entity_id(mock_node)
    state = hass.states.get(entity_id)
    # check basic properties
    assert state.object_id.startswith(
        get_object_id(get_boost_temperature_entity_name(mock_node))
    )
    assert state.entity_id.startswith(get_boost_temperature_entity_id(mock_node))
    assert state.name == f"{mock_node['name']} Boost temperature"
    assert (
        state.attributes[ATTR_FRIENDLY_NAME] == f"{mock_node['name']} Boost temperature"
    )
    unique_id = get_node_unique_id(mock_device, mock_node, "config_boost_temperature")
    assert entity_id == get_entity_id_from_unique_id(hass, NUMBER_DOMAIN, unique_id)
    await hass.services.async_call(
        NUMBER_DOMAIN,
        SERVICE_SET_VALUE,
        {ATTR_ENTITY_ID: entity_id, ATTR_VALUE: 25.0},
        blocking=True,
    )
    # Faut simuler le retour de la websocket
    await async_update_entity(hass, entity_id)
    state = hass.states.get(entity_id)
    assert state.state == "25.0"


async def test_boost_duration(hass, mock_smartbox, config_entry):
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert len(hass.states.async_entity_ids(NUMBER_DOMAIN)) == 11
    entries = hass.config_entries.async_entries(DOMAIN)
    assert len(entries) == 1

    assert DOMAIN in hass.config.components
    mock_device = (await mock_smartbox.session.get_devices())[1]
    mock_node = (await mock_smartbox.session.get_nodes(mock_device["dev_id"]))[3]
    entity_id = get_boost_duration_entity_id(mock_node)
    state = hass.states.get(entity_id)
    # check basic properties
    assert state.object_id.startswith(
        get_object_id(get_boost_duration_entity_name(mock_node))
    )
    assert state.entity_id.startswith(get_boost_duration_entity_id(mock_node))
    assert state.name == f"{mock_node['name']} Boost duration"
    assert state.attributes[ATTR_FRIENDLY_NAME] == f"{mock_node['name']} Boost duration"
    unique_id = get_node_unique_id(mock_device, mock_node, "config_boost_duration")
    assert entity_id == get_entity_id_from_unique_id(hass, NUMBER_DOMAIN, unique_id)
    await hass.services.async_call(
        NUMBER_DOMAIN,
        SERVICE_SET_VALUE,
        {ATTR_ENTITY_ID: entity_id, ATTR_VALUE: 120.0},
        blocking=True,
    )
    # Faut simuler le retour de la websocket
    await async_update_entity(hass, entity_id)
    state = hass.states.get(entity_id)
    assert state.state == "120.0"
