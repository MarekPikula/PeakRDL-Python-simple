"""Python abstraction for SystemRDL register description.

Don't override. Generated from:
    example/accelera-generic_example.rdl
"""

from enum import IntEnum

from peakrdl_python_simple.regif import access, spec


class ChipIdReg(access.RegAccess):
    """This chip part number and revision #

    This register cotains the part # and revision # for XYZ ASIC
    """

    part_num = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='part_num', type_name='part_num', orig_type_name=None, external=True, width=28, msb=31, lsb=4, high=31, low=4, is_virtual=False, is_volatile=True, is_sw_writable=False, is_sw_readable=True, is_hw_writable=True, is_hw_readable=False, implements_storage=False, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """This field represents the chips part number"""


class LinkStatusEnum(IntEnum):
    not_present = 0
    """No link peer is currently detected"""

    training = 1
    """Link is currently training"""

    snooze = 5
    """Link is in a partial low power state"""

    sleep = 6
    """Link is a Full low power state"""

    wake = 7
    """Link is waking up from snooze or sleep state"""

    active = 10
    """Link is opertating normally"""


class SerdesLinkStatusRegReg(access.RegAccess):
    port0 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='port0', type_name='link_status_field', orig_type_name='link_status_field', external=False, width=4, msb=3, lsb=0, high=3, low=0, is_virtual=False, is_volatile=True, is_sw_writable=False, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='LinkStatusEnum'), field_type=LinkStatusEnum)
    """Status of a Serdes Link"""

    port1 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='port1', type_name='link_status_field', orig_type_name='link_status_field', external=False, width=4, msb=7, lsb=4, high=7, low=4, is_virtual=False, is_volatile=True, is_sw_writable=False, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='LinkStatusEnum'), field_type=LinkStatusEnum)
    """Status of a Serdes Link"""

    port2 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='port2', type_name='link_status_field', orig_type_name='link_status_field', external=False, width=4, msb=11, lsb=8, high=11, low=8, is_virtual=False, is_volatile=True, is_sw_writable=False, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='LinkStatusEnum'), field_type=LinkStatusEnum)
    """Status of a Serdes Link"""

    port3 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='port3', type_name='link_status_field', orig_type_name='link_status_field', external=False, width=4, msb=15, lsb=12, high=15, low=12, is_virtual=False, is_volatile=True, is_sw_writable=False, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='LinkStatusEnum'), field_type=LinkStatusEnum)
    """Status of a Serdes Link"""


class MyRegReg(access.RegAccess):
    data0 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data0', type_name='myField_reset_0', orig_type_name='myField', external=False, width=2, msb=1, lsb=0, high=1, low=0, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """My example 2bit status field"""

    data1 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data1', type_name='myField_reset_1', orig_type_name='myField', external=False, width=2, msb=3, lsb=2, high=3, low=2, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """My example 2bit status field"""

    data2 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data2', type_name='myField_reset_2', orig_type_name='myField', external=False, width=2, msb=5, lsb=4, high=5, low=4, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """My example 2bit status field"""

    data3 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data3', type_name='myField_reset_3', orig_type_name='myField', external=False, width=2, msb=7, lsb=6, high=7, low=6, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """My example 2bit status field"""

    data4 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data4', type_name='myField_reset_0', orig_type_name='myField', external=False, width=2, msb=9, lsb=8, high=9, low=8, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """My example 2bit status field"""

    data5 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data5', type_name='myField_reset_1', orig_type_name='myField', external=False, width=2, msb=11, lsb=10, high=11, low=10, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """My example 2bit status field"""

    data6 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data6', type_name='myField_reset_2', orig_type_name='myField', external=False, width=2, msb=13, lsb=12, high=13, low=12, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """My example 2bit status field"""

    data7 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data7', type_name='myField_reset_3', orig_type_name='myField', external=False, width=2, msb=15, lsb=14, high=15, low=14, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """My example 2bit status field"""

    data8 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data8', type_name='myField_reset_0', orig_type_name='myField', external=False, width=2, msb=17, lsb=16, high=17, low=16, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """My example 2bit status field"""

    data9 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data9', type_name='myField_reset_1', orig_type_name='myField', external=False, width=2, msb=19, lsb=18, high=19, low=18, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """My example 2bit status field"""

    data10 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data10', type_name='myField_reset_2', orig_type_name='myField', external=False, width=2, msb=21, lsb=20, high=21, low=20, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """My example 2bit status field"""

    data11 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data11', type_name='myField_reset_3', orig_type_name='myField', external=False, width=2, msb=23, lsb=22, high=23, low=22, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """My example 2bit status field"""

    data12 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data12', type_name='myField_reset_0', orig_type_name='myField', external=False, width=2, msb=25, lsb=24, high=25, low=24, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """My example 2bit status field"""

    data13 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data13', type_name='myField_reset_1', orig_type_name='myField', external=False, width=2, msb=27, lsb=26, high=27, low=26, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """My example 2bit status field"""

    data14 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data14', type_name='myField_reset_2', orig_type_name='myField', external=False, width=2, msb=29, lsb=28, high=29, low=28, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """My example 2bit status field"""

    data15 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data15', type_name='myField_reset_3', orig_type_name='myField', external=False, width=2, msb=31, lsb=30, high=31, low=30, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)
    """My example 2bit status field"""


class Spi4PktCountRegReg(access.RegAccess):
    port1 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='port1', type_name='count_field_threshold_cfff', orig_type_name='count_field', external=False, width=16, msb=15, lsb=0, high=15, low=0, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=False, is_hw_readable=True, implements_storage=True, is_up_counter=True, is_down_counter=False, encode='int'), field_type=int)
    """Number of certain packet type seen"""

    port0 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='port0', type_name='count_field_threshold_cfff', orig_type_name='count_field', external=False, width=16, msb=31, lsb=16, high=31, low=16, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=False, is_hw_readable=True, implements_storage=True, is_up_counter=True, is_down_counter=False, encode='int'), field_type=int)
    """Number of certain packet type seen"""


class GigePktCountRegReg(access.RegAccess):
    port3 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='port3', type_name='count_field', orig_type_name='count_field', external=False, width=8, msb=7, lsb=0, high=7, low=0, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=False, is_hw_readable=True, implements_storage=True, is_up_counter=True, is_down_counter=False, encode='int'), field_type=int)
    """Number of certain packet type seen"""

    port2 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='port2', type_name='count_field', orig_type_name='count_field', external=False, width=8, msb=15, lsb=8, high=15, low=8, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=False, is_hw_readable=True, implements_storage=True, is_up_counter=True, is_down_counter=False, encode='int'), field_type=int)
    """Number of certain packet type seen"""

    port1 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='port1', type_name='count_field', orig_type_name='count_field', external=False, width=8, msb=23, lsb=16, high=23, low=16, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=False, is_hw_readable=True, implements_storage=True, is_up_counter=True, is_down_counter=False, encode='int'), field_type=int)
    """Number of certain packet type seen"""

    port0 = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='port0', type_name='count_field', orig_type_name='count_field', external=False, width=8, msb=31, lsb=24, high=31, low=24, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=False, is_hw_readable=True, implements_storage=True, is_up_counter=True, is_down_counter=False, encode='int'), field_type=int)
    """Number of certain packet type seen"""


class PointerRegDataC4c0841bReg(access.RegAccess):
    data = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data', type_name='data_resetsignal_7de55995', orig_type_name=None, external=False, width=32, msb=31, lsb=0, high=31, low=0, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)


class PointerRegReg(access.RegAccess):
    data = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='data', type_name='data', orig_type_name=None, external=False, width=32, msb=31, lsb=0, high=31, low=0, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='int'), field_type=int)


class FifoStatusRegReg(access.RegAccess):
    full = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='full', type_name='full_reset_0_resetsignal_7de55995', orig_type_name=None, external=False, width=1, msb=0, lsb=0, high=0, low=0, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='bool'), field_type=bool)
    empty = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='empty', type_name='empty_reset_1', orig_type_name=None, external=False, width=1, msb=1, lsb=1, high=1, low=1, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='bool'), field_type=bool)
    almost_empty = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='almost_empty', type_name='almost_empty_reset_1', orig_type_name=None, external=False, width=1, msb=4, lsb=4, high=4, low=4, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='bool'), field_type=bool)
    almost_full = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='almost_full', type_name='almost_full_reset_0', orig_type_name=None, external=False, width=1, msb=5, lsb=5, high=5, low=5, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='bool'), field_type=bool)


class FifoRfileRegfile(access.RegfileAccess):
    head = PointerRegDataC4c0841bReg(specification=spec.RegNodeSpec(inst_name='head', type_name='pointerReg_data_c4c0841b', orig_type_name='pointerReg', external=False, raw_address_offset=0, address_offset=0, raw_absolute_address=256, absolute_address=256, size=4, total_size=4, is_array=False, array_dimensions=None, array_stride=None, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    tail = PointerRegReg(specification=spec.RegNodeSpec(inst_name='tail', type_name='pointerReg', orig_type_name='pointerReg', external=False, raw_address_offset=4, address_offset=4, raw_absolute_address=260, absolute_address=260, size=4, total_size=4, is_array=False, array_dimensions=None, array_stride=None, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    status = FifoStatusRegReg(specification=spec.RegNodeSpec(inst_name='status', type_name='fifoStatusReg', orig_type_name='fifoStatusReg', external=False, raw_address_offset=8, address_offset=8, raw_absolute_address=264, absolute_address=264, size=4, total_size=4, is_array=False, array_dimensions=None, array_stride=None, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))


class VcPktCountRegReg(access.RegAccess):
    vc_count = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='vc_count', type_name='count_field_reset_0', orig_type_name='count_field', external=False, width=31, msb=30, lsb=0, high=30, low=0, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=False, is_hw_readable=True, implements_storage=True, is_up_counter=True, is_down_counter=False, encode='int'), field_type=int)
    """Number of certain packet type seen"""

    active = access.FieldAccess(specification=spec.FieldNodeSpec(inst_name='active', type_name='active_reset_1', orig_type_name=None, external=False, width=1, msb=31, lsb=31, high=31, low=31, is_virtual=False, is_volatile=True, is_sw_writable=True, is_sw_readable=True, is_hw_writable=True, is_hw_readable=True, implements_storage=True, is_up_counter=False, is_down_counter=False, encode='bool'), field_type=bool)
    """VC is Active"""


class SomeRegisterMapAddrmap(access.AddrmapAccess):
    """RDL Example Registers

    This address map contains some example registers to show
    how RDL can be utilized in various situations.
    """

    _spec = spec.AddrmapNodeSpec(inst_name='some_register_map', type_name='some_register_map', orig_type_name='some_register_map', external=True, raw_address_offset=0, address_offset=0, raw_absolute_address=0, absolute_address=0, size=4160, total_size=4160, is_array=False, array_dimensions=None, array_stride=None)
    chip_id_reg = ChipIdReg(specification=spec.RegNodeSpec(inst_name='chip_id_reg', type_name='chip_id', orig_type_name='chip_id', external=True, raw_address_offset=0, address_offset=0, raw_absolute_address=0, absolute_address=0, size=4, total_size=4, is_array=False, array_dimensions=None, array_stride=None, is_virtual=False, has_sw_writable=False, has_sw_readable=True, has_hw_writable=True, has_hw_readable=False, is_interrupt_reg=False, is_halt_reg=False))
    """This chip part number and revision #

    This register cotains the part # and revision # for XYZ ASIC
    """

    link_status = SerdesLinkStatusRegReg(specification=spec.RegNodeSpec(inst_name='link_status', type_name='serdes_link_status_reg', orig_type_name='serdes_link_status_reg', external=False, raw_address_offset=4, address_offset=4, raw_absolute_address=4, absolute_address=4, size=4, total_size=4, is_array=False, array_dimensions=None, array_stride=None, is_virtual=False, has_sw_writable=False, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    myRegInst = MyRegReg(specification=spec.RegNodeSpec(inst_name='myRegInst', type_name='myReg', orig_type_name='myReg', external=False, raw_address_offset=16, address_offset=16, raw_absolute_address=16, absolute_address=16, size=4, total_size=4, is_array=False, array_dimensions=None, array_stride=None, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    spi4_pkt_count = Spi4PktCountRegReg(specification=spec.RegNodeSpec(inst_name='spi4_pkt_count', type_name='spi4_pkt_count_reg', orig_type_name='spi4_pkt_count_reg', external=False, raw_address_offset=32, address_offset=32, raw_absolute_address=32, absolute_address=32, size=4, total_size=4, is_array=False, array_dimensions=None, array_stride=None, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=False, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    gige_pkt_count_reg = GigePktCountRegReg(specification=spec.RegNodeSpec(inst_name='gige_pkt_count_reg', type_name='gige_pkt_count_reg', orig_type_name='gige_pkt_count_reg', external=False, raw_address_offset=36, address_offset=36, raw_absolute_address=36, absolute_address=36, size=4, total_size=4, is_array=False, array_dimensions=None, array_stride=None, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=False, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    fifo_port_0 = FifoRfileRegfile(specification=spec.RegfileNodeSpec(inst_name='fifo_port', type_name='fifoRfile', orig_type_name='fifoRfile', external=False, raw_address_offset=256, address_offset=256, raw_absolute_address=256, absolute_address=256, size=12, total_size=128, is_array=True, array_dimensions=[8], array_stride=16))
    fifo_port_1 = FifoRfileRegfile(specification=spec.RegfileNodeSpec(inst_name='fifo_port', type_name='fifoRfile', orig_type_name='fifoRfile', external=False, raw_address_offset=256, address_offset=272, raw_absolute_address=256, absolute_address=272, size=12, total_size=128, is_array=True, array_dimensions=[8], array_stride=16))
    fifo_port_2 = FifoRfileRegfile(specification=spec.RegfileNodeSpec(inst_name='fifo_port', type_name='fifoRfile', orig_type_name='fifoRfile', external=False, raw_address_offset=256, address_offset=288, raw_absolute_address=256, absolute_address=288, size=12, total_size=128, is_array=True, array_dimensions=[8], array_stride=16))
    fifo_port_3 = FifoRfileRegfile(specification=spec.RegfileNodeSpec(inst_name='fifo_port', type_name='fifoRfile', orig_type_name='fifoRfile', external=False, raw_address_offset=256, address_offset=304, raw_absolute_address=256, absolute_address=304, size=12, total_size=128, is_array=True, array_dimensions=[8], array_stride=16))
    fifo_port_4 = FifoRfileRegfile(specification=spec.RegfileNodeSpec(inst_name='fifo_port', type_name='fifoRfile', orig_type_name='fifoRfile', external=False, raw_address_offset=256, address_offset=320, raw_absolute_address=256, absolute_address=320, size=12, total_size=128, is_array=True, array_dimensions=[8], array_stride=16))
    fifo_port_5 = FifoRfileRegfile(specification=spec.RegfileNodeSpec(inst_name='fifo_port', type_name='fifoRfile', orig_type_name='fifoRfile', external=False, raw_address_offset=256, address_offset=336, raw_absolute_address=256, absolute_address=336, size=12, total_size=128, is_array=True, array_dimensions=[8], array_stride=16))
    fifo_port_6 = FifoRfileRegfile(specification=spec.RegfileNodeSpec(inst_name='fifo_port', type_name='fifoRfile', orig_type_name='fifoRfile', external=False, raw_address_offset=256, address_offset=352, raw_absolute_address=256, absolute_address=352, size=12, total_size=128, is_array=True, array_dimensions=[8], array_stride=16))
    fifo_port_7 = FifoRfileRegfile(specification=spec.RegfileNodeSpec(inst_name='fifo_port', type_name='fifoRfile', orig_type_name='fifoRfile', external=False, raw_address_offset=256, address_offset=368, raw_absolute_address=256, absolute_address=368, size=12, total_size=128, is_array=True, array_dimensions=[8], array_stride=16))
    vc_pkt_count_0_0 = VcPktCountRegReg(specification=spec.RegNodeSpec(inst_name='vc_pkt_count', type_name='vc_pkt_count_reg', orig_type_name='vc_pkt_count_reg', external=False, raw_address_offset=4096, address_offset=4096, raw_absolute_address=4096, absolute_address=4096, size=4, total_size=64, is_array=True, array_dimensions=[8, 2], array_stride=4, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    vc_pkt_count_0_1 = VcPktCountRegReg(specification=spec.RegNodeSpec(inst_name='vc_pkt_count', type_name='vc_pkt_count_reg', orig_type_name='vc_pkt_count_reg', external=False, raw_address_offset=4096, address_offset=4100, raw_absolute_address=4096, absolute_address=4100, size=4, total_size=64, is_array=True, array_dimensions=[8, 2], array_stride=4, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    vc_pkt_count_1_0 = VcPktCountRegReg(specification=spec.RegNodeSpec(inst_name='vc_pkt_count', type_name='vc_pkt_count_reg', orig_type_name='vc_pkt_count_reg', external=False, raw_address_offset=4096, address_offset=4104, raw_absolute_address=4096, absolute_address=4104, size=4, total_size=64, is_array=True, array_dimensions=[8, 2], array_stride=4, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    vc_pkt_count_1_1 = VcPktCountRegReg(specification=spec.RegNodeSpec(inst_name='vc_pkt_count', type_name='vc_pkt_count_reg', orig_type_name='vc_pkt_count_reg', external=False, raw_address_offset=4096, address_offset=4108, raw_absolute_address=4096, absolute_address=4108, size=4, total_size=64, is_array=True, array_dimensions=[8, 2], array_stride=4, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    vc_pkt_count_2_0 = VcPktCountRegReg(specification=spec.RegNodeSpec(inst_name='vc_pkt_count', type_name='vc_pkt_count_reg', orig_type_name='vc_pkt_count_reg', external=False, raw_address_offset=4096, address_offset=4112, raw_absolute_address=4096, absolute_address=4112, size=4, total_size=64, is_array=True, array_dimensions=[8, 2], array_stride=4, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    vc_pkt_count_2_1 = VcPktCountRegReg(specification=spec.RegNodeSpec(inst_name='vc_pkt_count', type_name='vc_pkt_count_reg', orig_type_name='vc_pkt_count_reg', external=False, raw_address_offset=4096, address_offset=4116, raw_absolute_address=4096, absolute_address=4116, size=4, total_size=64, is_array=True, array_dimensions=[8, 2], array_stride=4, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    vc_pkt_count_3_0 = VcPktCountRegReg(specification=spec.RegNodeSpec(inst_name='vc_pkt_count', type_name='vc_pkt_count_reg', orig_type_name='vc_pkt_count_reg', external=False, raw_address_offset=4096, address_offset=4120, raw_absolute_address=4096, absolute_address=4120, size=4, total_size=64, is_array=True, array_dimensions=[8, 2], array_stride=4, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    vc_pkt_count_3_1 = VcPktCountRegReg(specification=spec.RegNodeSpec(inst_name='vc_pkt_count', type_name='vc_pkt_count_reg', orig_type_name='vc_pkt_count_reg', external=False, raw_address_offset=4096, address_offset=4124, raw_absolute_address=4096, absolute_address=4124, size=4, total_size=64, is_array=True, array_dimensions=[8, 2], array_stride=4, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    vc_pkt_count_4_0 = VcPktCountRegReg(specification=spec.RegNodeSpec(inst_name='vc_pkt_count', type_name='vc_pkt_count_reg', orig_type_name='vc_pkt_count_reg', external=False, raw_address_offset=4096, address_offset=4128, raw_absolute_address=4096, absolute_address=4128, size=4, total_size=64, is_array=True, array_dimensions=[8, 2], array_stride=4, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    vc_pkt_count_4_1 = VcPktCountRegReg(specification=spec.RegNodeSpec(inst_name='vc_pkt_count', type_name='vc_pkt_count_reg', orig_type_name='vc_pkt_count_reg', external=False, raw_address_offset=4096, address_offset=4132, raw_absolute_address=4096, absolute_address=4132, size=4, total_size=64, is_array=True, array_dimensions=[8, 2], array_stride=4, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    vc_pkt_count_5_0 = VcPktCountRegReg(specification=spec.RegNodeSpec(inst_name='vc_pkt_count', type_name='vc_pkt_count_reg', orig_type_name='vc_pkt_count_reg', external=False, raw_address_offset=4096, address_offset=4136, raw_absolute_address=4096, absolute_address=4136, size=4, total_size=64, is_array=True, array_dimensions=[8, 2], array_stride=4, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    vc_pkt_count_5_1 = VcPktCountRegReg(specification=spec.RegNodeSpec(inst_name='vc_pkt_count', type_name='vc_pkt_count_reg', orig_type_name='vc_pkt_count_reg', external=False, raw_address_offset=4096, address_offset=4140, raw_absolute_address=4096, absolute_address=4140, size=4, total_size=64, is_array=True, array_dimensions=[8, 2], array_stride=4, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    vc_pkt_count_6_0 = VcPktCountRegReg(specification=spec.RegNodeSpec(inst_name='vc_pkt_count', type_name='vc_pkt_count_reg', orig_type_name='vc_pkt_count_reg', external=False, raw_address_offset=4096, address_offset=4144, raw_absolute_address=4096, absolute_address=4144, size=4, total_size=64, is_array=True, array_dimensions=[8, 2], array_stride=4, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    vc_pkt_count_6_1 = VcPktCountRegReg(specification=spec.RegNodeSpec(inst_name='vc_pkt_count', type_name='vc_pkt_count_reg', orig_type_name='vc_pkt_count_reg', external=False, raw_address_offset=4096, address_offset=4148, raw_absolute_address=4096, absolute_address=4148, size=4, total_size=64, is_array=True, array_dimensions=[8, 2], array_stride=4, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    vc_pkt_count_7_0 = VcPktCountRegReg(specification=spec.RegNodeSpec(inst_name='vc_pkt_count', type_name='vc_pkt_count_reg', orig_type_name='vc_pkt_count_reg', external=False, raw_address_offset=4096, address_offset=4152, raw_absolute_address=4096, absolute_address=4152, size=4, total_size=64, is_array=True, array_dimensions=[8, 2], array_stride=4, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
    vc_pkt_count_7_1 = VcPktCountRegReg(specification=spec.RegNodeSpec(inst_name='vc_pkt_count', type_name='vc_pkt_count_reg', orig_type_name='vc_pkt_count_reg', external=False, raw_address_offset=4096, address_offset=4156, raw_absolute_address=4096, absolute_address=4156, size=4, total_size=64, is_array=True, array_dimensions=[8, 2], array_stride=4, is_virtual=False, has_sw_writable=True, has_sw_readable=True, has_hw_writable=True, has_hw_readable=True, is_interrupt_reg=False, is_halt_reg=False))
